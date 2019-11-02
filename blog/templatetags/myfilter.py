#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

from django import template
register = template.Library()

@register.filter
def month_to_upper(key):
    return ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'][key.month - 1]