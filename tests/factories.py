import factory.django

from ads.models import *
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    # password = factory.Faker("password")
    # age = 37
    # birth_date = "1985-02-24"
    email = factory.Faker("email")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("ean", length=8)


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker("name")
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    price = factory.Faker("ean", length=8)
