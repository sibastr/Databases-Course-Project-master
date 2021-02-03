from django.db import models
from django.conf import settings
from shop.models import Product
from django.urls import reverse


# OK
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Корзина {self.user.email}'

    def get_cart_items(self):
        return CartItem.objects.filter(cart=self).order_by('product')

    def get_total(self):
        total = 0
        for item in self.get_cart_items():
            total += item.get_full_cost()

        return round(total, 2)

    def get_final_total(self):
        total = 0
        for item in self.get_cart_items():
            total += item.get_full_final_cost()

        return round(total, 2)

    def get_item_number(self):
        number = 0
        for item in self.get_cart_items():
            number += item.quantity

        return number

    def is_empty(self):
        if len(self.get_cart_items()) == 0:
            return True
        else:
            return False

    def clear(self):
        self.get_cart_items().delete()


# OK
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} in cart of {self.cart.user.email}'

    def get_final_cost(self):
        if self.product.on_sale:
            return round(((100 - self.product.discount) / 100 * self.product.cost) * (100 - self.cart.user.profile.loyalty_card.discount) / 100, 2)
        else:
            return round(self.product.cost * (100 - self.cart.user.profile.loyalty_card.discount) / 100, 2)

    def get_full_cost(self):
        if self.product.on_sale:
            return round(((100 - self.product.discount) / 100 * self.product.cost) * self.quantity, 2)
        else:
            return round(self.product.cost * self.quantity, 2)

    def get_full_final_cost(self):
        if self.product.on_sale:
            return round(((100 - self.product.discount) / 100 * self.product.cost) * self.quantity * (100 - self.cart.user.profile.loyalty_card.discount) / 100, 2)
        else:
            return round(self.product.cost * self.quantity * (100 - self.cart.user.profile.loyalty_card.discount) / 100, 2)


# OK
class Order(models.Model):
    CARD = 'card'
    CASH = 'cash'
    PAYMENT_CHOICES = [
        (CARD, 'Карта'),
        (CASH, 'Наличные')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(
        max_length=4,
        choices=PAYMENT_CHOICES,
        default=CASH
    )
    address = models.CharField(max_length=250, default='')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Order id: {self.id} of user {self.user.email}'

    def get_absolute_url(self):
        return reverse('shop-home')

    def get_ru_payment(self):
        name_ru = ''
        if self.payment_method == 'card':
            name_ru = 'Картой'
        elif self.payment_method == 'cash':
            name_ru = 'Наличными'

        return name_ru

    def get_total(self):
        total = 0
        for item in OrderItem.objects.filter(order=self.id):
            total += item.get_full_cost()
        return total

    def get_final_total(self):
        total = 0
        for item in OrderItem.objects.filter(order=self.id):
            total += item.get_full_final_cost()
        return total

    def get_order_items(self):
        return OrderItem.objects.filter(order=self).order_by('product')


    # OK
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    item_cost = models.FloatField()
    item_cost_final = models.FloatField()

    def __str__(self):
        return f'{self.product.name} in order id:{self.order.id} of {self.order.user.email}'

    def get_full_cost(self):
        return round(self.item_cost * self.quantity, 2)

    def get_full_final_cost(self):
        return round(self.item_cost_final * self.quantity, 2)
