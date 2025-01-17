from django.urls import path
from .views import BrandListView, RegisterView, LoginView, LogoutView

from . import views

urlpatterns = [
    # path("", views.BrandViewSet, name="brands"),
    # path("<int:brand_id>/", views.detail, name="detail"),
    # path("brands/", views.brands, name='brands'),
    path('api/brands/', BrandListView.as_view(), name='brand-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]