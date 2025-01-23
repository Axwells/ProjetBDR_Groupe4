from django.urls import path
from .views import BrandListView, RegisterView, LoginView, LogoutView, SpecificationsByCarView, CarDetailsView, SearchCarsView, ReviewsBySpecificationView, AddReviewView, AddModificationView, GetModificationsView, UpdateModificationView, UserListView, CreateUserView, UpdateUserView, DeleteUserView
from . import views

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('specifications/<str:model_name_car>/', SpecificationsByCarView.as_view(), name='specifications-by-car'),
    path('cars/details/<str:model_name_car>/', CarDetailsView.as_view(), name='car-details'),
    path("search", SearchCarsView.as_view(), name="search-cars"),
    path('reviews/<int:spec_id>/', ReviewsBySpecificationView.as_view(), name='reviews-by-specification'),
    path('reviews/add/', AddReviewView.as_view(), name='add-review'),
    path('modifications/add/', AddModificationView.as_view(), name='add-modification'),
    path("modifications/", GetModificationsView.as_view(), name="get-modifications"),
    path("modifications/<int:modification_id>/", UpdateModificationView.as_view(), name="update-modification"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/add/", CreateUserView.as_view(), name="create-user"),
    path("users/update/<str:email>/", UpdateUserView.as_view(), name="update-user"),
    path("users/delete/<str:email>/", DeleteUserView.as_view(), name="delete-user"),
]