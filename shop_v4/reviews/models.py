from django.db import models
from django.conf import settings
from django.urls import reverse


class Review(models.Model):
	class Rating(models.IntegerChoices):
		ONE = 1
		TWO = 2
		THREE = 3
		FOUR = 4
		FIVE = 5

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
	rating = models.IntegerField(choices=Rating.choices)
	advantages = models.TextField()
	disadvantages = models.TextField()
	review = models.TextField()
	date_posted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Отзыв {self.user.email} о {self.product.name}'

	# Нужно для редиректа после заполнения формы
	def get_absolute_url(self):
		return reverse('shop-product', kwargs={'pk': self.product.id})
