from dateutil.relativedelta import relativedelta
from django.utils.text import slugify
import factory
import faker

from .models import Program, Host, Episode

faker = faker.Factory.create()


class ProgramFactory(factory.DjangoModelFactory):
    class Meta:
        model = Program

    name = factory.Faker('company')

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class HostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Host


class EpisodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Episode

    program = factory.SubFactory(ProgramFactory)
    number = factory.Sequence(lambda n: n)
    slug = factory.Sequence(lambda n: 'slug-' + str(n))
