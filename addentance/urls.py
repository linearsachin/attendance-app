from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(),name = "home"),
    path('class/<pk>/<subject_pk>', views.ClassView.as_view(), name="class"),


]
