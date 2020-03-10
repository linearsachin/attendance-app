from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(),name = "home"),
    path('class/<pk>/<subject_pk>', views.ClassView.as_view(), name="class"),
    path('mark/<pk>/<subject_pk>', views.MarkAttendanceView.as_view(), name="mark-attendance"),
    path('detailed/<class_pk>/<subject_pk>', views.DetailedAttendance.as_view(), name="detailed-attendance"),
    path('export/<class_pk>/<subject_pk>', views.export_users_csv, name='export_users_csv'),
    path('defaulters/<class_pk>/<subject_pk>', views.Defaulters.as_view(), name='defaulter-list'),


]
