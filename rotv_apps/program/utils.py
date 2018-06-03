from django.utils.text import slugify


def get_slug(Model, title):
    first_slug_proposal = slug_proposal = slugify(title)
    n = 1
    while Model.objects.filter(slug=slug_proposal).count():
        slug_proposal = first_slug_proposal + "-{}".format(n)
        n += 1

    return slug_proposal
