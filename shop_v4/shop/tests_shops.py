import os
import django
import sys

sys.path.append(r'C:\Users\sibas\Desktop\study\Databases-Course-Project-master\shop_v4\shop_v3')
sys.path.append(r'C:\Users\sibas\Desktop\study\Databases-Course-Project-master\shop_v4')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
from django.test import TestCase

from shop.models import Product, Category, Color, Feature, FeatureVariant, FeatureSet
sys.path.append("C:/Users/sibas/Desktop/study/Databases-Course-Project-master/shop_v4/users/models.py")
from users.models import MyUser
from shop.data_builders import ColorBuilder, CategoryBuilder, UserBuilder
from unittest.mock import Mock, patch
from users.models import LoyaltyCard, Profile
from users.admin import UserCreationForm
from users.views import register

class ShopsTestCase(TestCase):
    def setUp(self):
        self.mocked_model = Mock()
        builder = ColorBuilder()
        builder.with_name('TestColor')
        record = builder.build()


    def test_Color1(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)


    def test_Color2(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)


    def test_Color3(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)


    def test_Color4(self):
        test_color = Color()
        test_color.name = "blue"
        something = "blue"
        self.assertEqual(test_color.name, something)


    def test_Color5(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)

    def test_Color6(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)


    def test_Color7(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)


    def test_Color8(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)

    def test_Color9(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)

    def test_Color10(self):
        test_color = Color()
        test_color.name = "green"
        something = "green"
        self.assertEqual(test_color.name, something)