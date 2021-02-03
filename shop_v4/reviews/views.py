from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Review
from shop.models import Product


class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    fields = ['rating', 'advantages', 'disadvantages', 'review']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.id in Product.objects.get(id=self.kwargs['pk']).get_reviews().values_list('user', flat=True):
            return False
        if not Product.objects.get(id=self.kwargs['pk']).displayed:
            return False
        return True


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['rating', 'advantages', 'disadvantages', 'review']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product = Product.objects.get(id=self.kwargs['prod'])
        return super().form_valid(form)

    def test_func(self):
        if self.request.user == self.get_object().user:
            return True
        return False


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'

    def test_func(self):
        if self.request.user == self.get_object().user:
            return True
        return False
