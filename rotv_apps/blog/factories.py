from django.utils.text import slugify
import factory
import faker

from .models import Entry, Category

fake = faker.Factory.create()


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('text', max_nb_chars=30)

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)


class EntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Entry

    title = factory.Faker('text', max_nb_chars=255)
    text = factory.Faker('paragraphs', nb=3)
    image_right = None

    @factory.lazy_attribute
    def new_tags(self):
        return ", ".join([word for word in fake.words()])

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.title)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)
