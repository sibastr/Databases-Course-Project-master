from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from cart.models import Order, Cart


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class LoyaltyCard(models.Model):
    name = models.CharField(max_length=50)
    discount = models.FloatField()

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    loyalty_card = models.ForeignKey(LoyaltyCard, on_delete=models.SET_NULL, null=True, default=6)



    def __str__(self):
        return f'{self.user.email} Profile'

    def upgrade_loyalty_card_by_one_level(self):
        card = self.loyalty_card.name
        if card != 'Алмазный':
            if card == 'Отсутствует':
                next_cart = 'Бронзовый'
            elif card == 'Бронзовый':
                next_cart = 'Серебряный'
            elif card == 'Серебряный':
                next_cart = 'Золотой'
            elif card == 'Золотой':
                next_cart = 'Платиновый'
            elif card == 'Платиновый':
                next_cart = 'Алмазный'
            self.loyalty_card = LoyaltyCard.objects.get(name=next_cart)
            self.save()

    def upgrade_loyalty_card(self):
        spent = 0
        for order in Order.objects.filter(user=self.user):
            if order:
                spent += order.get_final_total()

        if self.loyalty_card.name != 'Алмазный' or spent != 0:
            arr = [[0, 10000, 40000, 70000, 150000, 300000],
                   ['Отсутствует', 'Бронзовый', 'Серебряный', 'Золотой', 'Платиновый', 'Алмазный']]
            n = len(arr[0])

            for i in range(n - 1, -1, -1):
                if spent >= arr[0][i]:
                    new_limit = arr[0][i]
                    new_level = arr[1][arr[0].index(new_limit)]

                    if arr[0][arr[1].index(self.loyalty_card.name)] <= arr[0][arr[1].index(new_level)]:
                        self.loyalty_card = LoyaltyCard.objects.get(name=new_level)
                        self.save()
