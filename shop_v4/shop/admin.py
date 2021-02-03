from django.contrib import admin
from .models import Product, Category, Color, Feature, FeatureVariant, FeatureSet


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Feature)
admin.site.register(FeatureVariant)
admin.site.register(FeatureSet)
