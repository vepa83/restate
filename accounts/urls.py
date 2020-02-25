from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name="accounts"
urlpatterns = [
    path('profile/', views.ProfileView, name="profile"),
    path('profile/createad', views.create_adview, name="adcreate_url"),
    path('profile/update_profile/', views.update_profile, name="update_profile"),
    path('profile/create_profile/', views.create_profile, name="create_profile"),
    path('profile/adupdate<int:ad_id>/', views.update_ad, name="adupdate_url"),
    path('profile/add_image/<int:ad_id>/', views.add_imageview, name="addimage_url"),
    path('profile/delete_image/<int:image_id>/', views.delete_imageview, name="deleteimage_url"),
    path('login/', LoginView.as_view(), name="login_url"),
    path('register/', views.RegisterView, name='register_url'),
    path('logout/', LogoutView.as_view(next_page="accounts:login_url"), name="logout"),
]
