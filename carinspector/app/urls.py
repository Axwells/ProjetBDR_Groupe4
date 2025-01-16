from django.urls import path
from .views import BrandListView

from . import views

urlpatterns = [
    # path("", views.BrandViewSet, name="brands"),
    # path("<int:brand_id>/", views.detail, name="detail"),
    # path("brands/", views.brands, name='brands'),
    path('api/brands/', BrandListView.as_view(), name='brand-list'),
]