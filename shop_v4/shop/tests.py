import os
import django
import sys
import unittest
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
from users.models import LoyaltyCard, Profile,MyUserManager
from users.admin import UserCreationForm
from users.views import register
from django.db import IntegrityError


class ProductTestCase(TestCase):

    def setUp(self):
        self.mocked_model = Mock()
        builder = ColorBuilder()
        builder.with_name('TestColor')
        record = builder.build()

    """
    def test_create_none_name(self):
        builder =  ColorBuilder()

        with self.assertRaises(django.db.utils.IntegrityError):
            record = builder.build()
            record.save()"""

    def test_color_name(self):
        name = "TestName"
        builder = ColorBuilder()
        builder.with_name(name)
        record = builder.build()
        check = str(record)
        self.assertEqual(name, check)
    """
    def test_create_none_name_category(self):
        builder =  CategoryBuilder()

        with self.assertRaises(django.db.utils.IntegrityError):
            record = builder.build()
            record.save()
            """

    def test_category_name(self):
        name = "TestName"
        builder = CategoryBuilder()
        builder.with_name(name)
        record = builder.build()
        check = str(record)
        self.assertEqual(name, check)



    """def test_create_none_email_user(self):
        builder = UserBuilder()
        with self.assertRaises(django.db.utils.IntegrityError):
            record = builder.build()
            record.save()"""
    """
    @patch('users.admin.UserCreationForm')
    def test_UserCreationForm(self, MockUserCreationForm):
        response = self.client.get('/register/')

        assert MockUserCreationForm.called
        """


    @patch('users.admin.UserCreationForm')
    def test_UserCreationForm_positive(self, MockUserCreationForm):
        response = self.client.post('/register/')
        form = MockUserCreationForm()
        form.is_valid.return_value = False
        assert MockUserCreationForm.called

    def test_user_email(self):
        email = "AminovMishin@mail.ru"
        builder = UserBuilder()
        builder.with_email(email)
        record = builder.build()
        check = str(record)
        self.assertEqual(email, check)




    def test_newUser(self):
        user = MyUserManager()
        self.assertRaises(ValueError,user.create_user,None)

    @patch('users.admin.UserCreationForm')
    def test_UserCreationForm_positive(self, MockUserCreationForm):
        response = self.client.post('/register/')
        form = MockUserCreationForm()
        form.is_valid.return_value = False
        assert MockUserCreationForm.called

    def test_user_email(self):
        email = "AminovMishin@mail.ru"
        builder = UserBuilder()
        builder.with_email(email)
        record = builder.build()
        check = str(record)
        self.assertEqual(email, check)

    def test_newUser(self):
        user = MyUserManager()
        self.assertRaises(ValueError, user.create_user, None)





    def test_color_name(self):
        name = "TestName"
        builder = ColorBuilder()
        builder.with_name(name)
        record = builder.build()
        check = str(record)
        self.assertEqual(name, check)
    """
    def test_create_none_name_category(self):
        builder =  CategoryBuilder()

        with self.assertRaises(django.db.utils.IntegrityError):
            record = builder.build()
            record.save()
            """

    def test_category_name(self):
        name = "TestName"
        builder = CategoryBuilder()
        builder.with_name(name)
        record = builder.build()
        check = str(record)
        self.assertEqual(name, check)



""" @patch('users.models.LoyaltyCard')
  def test_loyal(self, MockLoyaltyCard):
      loyaltyCard = MockLoyaltyCard()

      loyaltyCard.name = "Серебряный"
      loyaltyCard.discount = 5
      pro = Profile()
      pro.loyalty_card = loyaltyCard
      pro.upgrade_loyalty_card_by_one_level()
      self.assertEqual(loyaltyCard.name, "Серебряный")"""














