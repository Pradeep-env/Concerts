from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.userlist, name="userlist"),
    path("users/signup", views.signup_user, name="signup_user"),
    path("users/profile", views.complete_profile, name="complete_profile"),
    path("users/profile/update", views.update_profile, name="update_profile"),
    path("users/login", views.login_user, name="login_user"),
]