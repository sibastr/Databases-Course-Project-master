from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView, ReviewDeleteView


urlpatterns = [
    path('product/<int:pk>/rev-create/', ReviewCreateView.as_view(), name='review-create'),
    path('product/<int:prod>/<int:pk>/rev-update/', ReviewUpdateView.as_view(), name='review-update'),
    path('product/<int:prod>/<int:pk>/rev-delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
