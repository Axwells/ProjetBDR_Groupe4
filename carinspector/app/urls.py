from django.urls import path
from .views import BrandListView, RegisterView, LoginView, LogoutView, CarsByBrandView

from . import views

urlpatterns = [
    # path("", views.BrandViewSet, name="brands"),
    # path("<int:brand_id>/", views.detail, name="detail"),
    # path("brands/", views.brands, name='brands'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('brands/<str:brand_name>/cars/', CarsByBrandView.as_view(), name='cars_by_brand'),
]