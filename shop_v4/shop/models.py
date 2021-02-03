from django.db import models
from django.conf import settings
from reviews.models import Review


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_features(self):
        return Feature.objects.filter(category=self)

    def get_products(self):
        return Product.objects.filter(category=self)

    def get_displayed_products(self):
        return Product.objects.filter(category=self, displayed=True)

    def get_stock_products(self):
        return Product.objects.filter(category=self, in_stock=True)

    def get_displayed_stock_products(self):
        return Product.objects.filter(category=self, displayed=True, in_stock=True)


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    cost = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(default='product_default.jpg', upload_to='product_pics')
    displayed = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_reviews(self):
        return Review.objects.filter(product=self)

    def get_sale_cost(self):
        return round((100 - self.discount) / 100 * self.cost)


class Feature(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    CHECKBOX = 'checkbox'
    RADIOBUTTON = 'radiobutton'
    TYPES = [
        (CHECKBOX, 'Множественный выбор'),
        (RADIOBUTTON, 'Одиночный выбор')
    ]

    type = models.CharField(
        max_length=11,
        choices=TYPES,
        default=CHECKBOX
    )

    def __str__(self):
        return self.category.name + ' - ' + self.name

    def get_variants(self):
        return FeatureVariant.objects.filter(feature=self)



class FeatureVariant(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.feature.category.name + ' - ' + self.feature.name + ' - ' + self.name


class FeatureSet(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature_variant = models.ForeignKey(FeatureVariant, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + ' - ' + self.feature_variant.name
