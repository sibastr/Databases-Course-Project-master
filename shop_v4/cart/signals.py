from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart, CartItem, Order, OrderItem
from users.models import MyUser


@receiver(post_save, sender=MyUser)
def create_cart(sender, instance, created, **kwargs):
	if created:
		cart = Cart(user=instance)
		cart.save()
		print('CART CREATED AND SAVED')


@receiver(post_save, sender=Order)
def create_order_items(sender, instance, created, **kwargs):
	if created:
		cart = Cart.objects.get(user=instance.user)

		# Переносим товары из корзины в заказ
		for cart_item in cart.get_cart_items():
			new_order_item = OrderItem(order=instance, product=cart_item.product, quantity=cart_item.quantity,
										item_cost=cart_item.product.cost, item_cost_final=cart_item.get_final_cost())
			new_order_item.save()

		# Удаляем товары из корзины
		cart.clear()

		instance.user.profile.upgrade_loyalty_card()
