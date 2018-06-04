import factory
from django.contrib.auth.models import User

from .models import ShortenedURL


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = True
    is_staff = True
    is_active = True


class ShortenedURLFactory(factory.DjangoModelFactory):
    class Meta:
        model = ShortenedURL

    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    url = factory.Sequence(lambda n: 'http://lvh.me/{}'.format(n))
