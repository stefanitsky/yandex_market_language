from yandex_market_language.models import Category
from faker import Faker


fake = Faker()


def create_random_category(
    category_id=str(fake.pyint()),
    name=fake.pystr(),
    parent_id=str(fake.pyint())
):
    return Category(category_id, name, parent_id)


CategoryFactory = create_random_category
