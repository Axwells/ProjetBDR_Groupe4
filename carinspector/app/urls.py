from django.urls import path

from . import views

urlpatterns = [
    # path("", views.BrandViewSet, name="brands"),
    path("<int:brand_id>/", views.detail, name="detail"),
]