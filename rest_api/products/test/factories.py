import factory
import random

class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'products.Product'
        django_get_or_create = ('sku',)

    id = factory.Sequence(lambda n: n)
    sku = factory.Sequence(lambda n: f'testproductsku{n}')
    name = factory.Sequence(lambda n: f'testname{n}')
    qty = random.randrange(0, 1001)
    price = round(random.uniform(0.00, 9999.99),2)