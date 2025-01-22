from django.urls import path
from .views import BrandListView, RegisterView, LoginView, LogoutView, CarsByBrandView, SpecificationsByCarView, CarDetailsView

from . import views

urlpatterns = [
    # path("", views.BrandViewSet, name="brands"),
    # path("<int:brand_id>/", views.detail, name="detail"),
    # path("brands/", views.brands, name='brands'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cars/<str:brand_name>/', CarsByBrandView.as_view(), name='cars-by-brand'),
    path('specifications/<str:model_name_car>/', SpecificationsByCarView.as_view(), name='specifications-by-car'),
    path('cars/details/<str:model_name_car>/', CarDetailsView.as_view(), name='car-details'),
]