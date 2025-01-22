from django.urls import path
from .views import BrandListView, RegisterView, LoginView, LogoutView, SpecificationsByCarView, CarDetailsView, SearchCarsView
from . import views

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('specifications/<str:model_name_car>/', SpecificationsByCarView.as_view(), name='specifications-by-car'),
    path('cars/details/<str:model_name_car>/', CarDetailsView.as_view(), name='car-details'),
    path("search", SearchCarsView.as_view(), name="search-cars"),
]