import logging

from django.db.models import Count
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

from blog.models import Category, Article, Comment

logger = logging.getLogger('blog.views')


# Create your views here.
def global_settings(request):
    # 站点基本信息
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    WEIBO_SINA = settings.WEIBO_SINA
    WEIBO_TENCENT = settings.WEIBO_TENCENT
    PRO_RSS = settings.PRO_RSS
    PRO_EMAIL = settings.PRO_EMAIL
    # 分类信息获取（导航数据）
    category_list = Category.objects.all()

    # 文章归档
    archive_list = Article.objects.distinct_date()

    # 广告数据

    # 标签云数据

    # 友情链接数据

    # 文章排行榜数据

    # 评论排行
    comment_count_list = Comment.objects.values('article').annotate(num_count=Count('article')).order_by('-num_count')[
                         :6]
    article_comment_order_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]

    return locals()


def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()
        article_list = getPage(request, article_list)
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
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())


# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list
