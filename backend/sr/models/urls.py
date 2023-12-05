from django.urls import path

from . import views

urlpatterns = [
    path("inference/", views.edsr, name="edsr.inference"),
    path("take_pic/", views.take_pic, name="edsr.take_pic"),
]