# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import truncatewords
from django.utils.http import urlquote_plus

register = template.Library()


@register.filter('read_more')
def read_more(body, absolute_url, truncate_limit=120):
    """
    This one was taken from: https://djangosnippets.org/snippets/841/
    """
    if '<!--more-->' in body:
        return body[:body.find('<!--more-->')]+'<a href="'+str(absolute_url)+'">Czytaj dalej</a>'
    else:
        return truncatewords(body, truncate_limit)+'<p><a href="'+str(absolute_url)+'">Czytaj dalej</a></p>'
