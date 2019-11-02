import logging

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

from blog.forms import CommentForm, LoginForm, RegisterForm
from blog.models import Category, Article, Comment, User

logger = logging.getLogger('blog.views')


# Create your views here.
def global_settings(request):
    # 站点基本信息
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # WEIBO_SINA = settings.WEIBO_SINA
    # WEIBO_TENCENT = settings.WEIBO_TENCENT
    # PRO_RSS = settings.PRO_RSS
    # PRO_EMAIL = settings.PRO_EMAIL
    # 分类信息获取（导航数据）
    category_list = Category.objects.all()
    # 文章归档
    archive_list = Article.objects.distinct_date()
    # 广告数据
    # 标签云数据
    # 友情链接数据
    # 文章排行榜数据（浏览量 和 站长推荐）
    # 评论排行
    comment_count_list = Comment.objects.values('article').annotate(num_count=Count('article')).order_by('-num_count')[
                         :6]
    article_comment_order_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    return locals()


def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()
        article_list = __get_pagination(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())


def archive(request):
    try:
        # 通过年和月进行过滤 - 得出Article
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        # 文章查询 - 通过归档的年和月
        article_list = Article.objects.filter(date_publish__icontains=year + '-' + month)
        article_list = __get_pagination(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())


# 按照标签查询对应的文章列表
def tag(request):
    try:
        pass
    except Exception as e:
        logger.error(e)


# 分页代码
def __get_pagination(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


# 文章详情页
def article(request):
    try:
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated else {'article': id})

        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'article.html', locals())


def category(request):
    try:
        # 获取用户提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = __get_pagination(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())


# 提交表单
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data['author'],
                                             email=comment_form.cleaned_data['email'],
                                             url=comment_form.cleaned_data['url'],
                                             content=comment_form.cleaned_data['comment'],
                                             article_id=comment_form.cleaned_data['article'],
                                             user=request.user if request.user.is_authenticated else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    # user.backend = 'django.contrib.auth.backend.ModelBackend' #指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'login.html', locals())


# 登出
def do_logout(request):
    try:
        logout(request)
        print(request.META['HTTP_REFERER'])
    except Exception as e:
        print(e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                # 注册
                user = User.objects.create(username=register_form.cleaned_data['username'],
                                           email=register_form.cleaned_data['email'],
                                           url=register_form.cleaned_data['url'],
                                           password=make_password(register_form.cleaned_data['password']), )
                user.save()
                # 登录
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': register_form.errors})
        else:
            register_form = RegisterForm()
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'reg.html', locals())
