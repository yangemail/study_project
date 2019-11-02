#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': 'required', }),
                               max_length=50,
                               error_messages={'required': 'Username不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'planceholder': 'Password', 'required': 'required'}),
                               max_length=20,
                               error_messages={'required': 'Password不能为空'})


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': 'required', }),
                               max_length=50,
                               error_messages={'required': 'username不能为空', })
    email = forms.EmailField(widget=forms.TextInput(attrs={'planceholder': 'Email', 'required': 'required', }),
                             max_length=50,
                             error_messages={'required': 'Email不能为空'})
    url = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Url', }),
                         max_length=100,
                         required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'required', }),
                               max_length=20,
                               error_messages={'required': 'Password不能为空'})


# 评论表单
class CommentForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput(
        attrs={"id": "author", "class": "comment_input", "required": "required", "size": "25", "tabindex": "1"}),
        max_length=50,
        error_messages={"required": "username不能为空", })
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"id": "email", "type": "email", "class": "comment_input", "required": "required", "size": "25",
               "tabindex": "2"}),
                             max_length=50,
                             error_messages={"required": "email不能为空", })
    url = forms.URLField(widget=forms.TextInput(attrs={"id": "url", "type": "url", "class": "comment_input",
                                                       "size": "25", "tabindex": "3"}),
                         max_length=100,
                         required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id": "comment", "class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),
                              max_length=200,
                              error_messages={"required": "评论不能为空", })
    article = forms.CharField(widget=forms.HiddenInput())
