from django import forms
from .models import Cart, CartItem


class CartChangeForm(forms.ModelForm):
	class Meta:
		model = Cart


class CartItemChangeForm(forms.ModelForm):
	class Meta:
		model = CartItem
		fields = ['quantity']
