from dateutil.relativedelta import relativedelta
from factory import DjangoModelFactory, lazy_attribute
import faker

from .models import Partner, MediaPatron, MediaPatronage, NormalMediaPatronage, Colaborator

faker = faker.Factory.create()


class MediaPatronageFactory(DjangoModelFactory):
    class Meta:
        model = MediaPatronage

    @lazy_attribute
    def start(self):
        return faker.date_time_between(start_date="+20d", end_date="+30d")

    @lazy_attribute
    def end(self):
        return self.start + relativedelta(days=3)

    name = lazy_attribute(lambda o: faker.company())
    url = lazy_attribute(lambda o: faker.url())
    active = True


class NormalMediaPatronage(DjangoModelFactory):
    class Meta:
        model = NormalMediaPatronage

    @lazy_attribute
    def start(self):
        return faker.date_time_between(start_date="+20d", end_date="+30d")

    @lazy_attribute
    def end(self):
        return self.start + relativedelta(days=3)

    name = lazy_attribute(lambda o: faker.company())
    url = lazy_attribute(lambda o: faker.url())
    active = True


class PartnerFactory(DjangoModelFactory):
    class Meta:
        model = Partner

    name = lazy_attribute(lambda o: faker.company())
    url = lazy_attribute(lambda o: faker.url())
    active = True


class MediaPatronFactory(DjangoModelFactory):
    class Meta:
        model = MediaPatron

    name = lazy_attribute(lambda o: faker.company())
    url = lazy_attribute(lambda o: faker.url())
    active = True


class ColaboratorFactory(DjangoModelFactory):
    class Meta:
        model = Colaborator

    name = lazy_attribute(lambda o: faker.company())
    url = lazy_attribute(lambda o: faker.url())
    active = True

