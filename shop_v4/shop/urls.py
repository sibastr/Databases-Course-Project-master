from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCategoryDetailView


urlpatterns = [
    path('', ProductListView.as_view(), name='shop-home'),
    path('category/<int:pk>/', ProductCategoryDetailView.as_view(), name='shop-category'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='shop-product')
]
