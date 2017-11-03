from dateutil.relativedelta import relativedelta
from django.utils.text import slugify
import factory
import faker

from .models import Hero, HeroEntry

faker = faker.Factory.create()


class HeroFactory(factory.DjangoModelFactory):
    class Meta:
        model = Hero

    name = factory.Faker('words')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class HeroEntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = HeroEntry

    hero = factory.SubFactory(HeroFactory)
    title = factory.Faker('words')
    subtitle = factory.Faker('words')
    text = factory.Faker('paragraph')
    url = factory.Faker('url')
    image = factory.Faker('file_path', extension='jpg')
