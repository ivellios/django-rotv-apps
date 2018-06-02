import os
import sys
import django

from django.conf import settings
from django.test.utils import get_runner


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['rotv_apps.blog',
                                      'rotv_apps.heros',
                                      'rotv_apps.navigations',
                                      'rotv_apps.partners',
                                      'rotv_apps.program',
                                      'rotv_apps.tag_search',
                                      ])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
