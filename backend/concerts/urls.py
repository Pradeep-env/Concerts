from django.urls import path
from . import views

urlpatterns = [
    path("concerts/create", views.create_concert, name="create_concert"),
    path("concerts/edit/<int:pk>/", views.concert_detail_action, name="concert_detail_action"),
]