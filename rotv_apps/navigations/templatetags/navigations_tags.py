# -*- coding: utf-8 -*-
from django import template

from ..models import Nav

register = template.Library()


@register.inclusion_tag('navigations/nav.html')
def navigation(slug):
    try:
        nav = Nav.objects.get(slug = slug, )
        elements = Nav.objects.active().filter(parent = nav)
        return {'nav': elements }
    except Nav.DoesNotExist:
        return None
