# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

NAV_TYPES = [
        [1, 'Normalne'],
        [2, 'Z ilustracjami'],
    ]


class NavQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)


class NavManager(models.Manager):
    pass


class Nav(models.Model):
    parent = models.ForeignKey('self', null = True, blank = True, related_name='subnav')
    name = models.CharField(_(u'Nazwa'), max_length = 255)
    slug = models.SlugField(_(u'Identyfikator slug'), )
    url = models.CharField(_(u'URL'), max_length = 255, blank = True, null = True)
    image = models.ImageField(_(u'Obraz w nawigacji'), upload_to = 'nav', null = True, blank = True, )
    order = models.IntegerField(_(u'Kolejność'), default = 100)
    subnav_type = models.PositiveIntegerField(_(u'Typ podmenu'), choices = NAV_TYPES, 
                                                blank = True, null = True
                                                )
    active = models.BooleanField(_(u'Aktywny'), default = True)

    objects = NavManager.from_queryset(NavQuerySet)()

    class Meta:
        verbose_name = _(u'Element nawigacji klasycznej')
        verbose_name_plural = _(u'Elementy nawigacji klasycznej')
        ordering = ['order', 'name', ]

    def __unicode__(self):
        return self.name + ' in ' + ( self.parent.name if self.parent else 'ROOT' )

    def is_root(self):
        return not self.parent

    def has_subnav(self):
        return bool(self.subnav_type) and self.subnav.count()

    def get_subnav(self):
        return self.subnav.active()
