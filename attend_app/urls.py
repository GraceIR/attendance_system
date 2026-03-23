# attend_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attendance-data/', views.attendance_data, name='attendance_data'),
    path('delete/<int:pk>/', views.delete_attendance, name='delete_attendance'),
    path('edit/<int:pk>/', views.edit_attendance, name='edit_attendance'),
    path('export-csv/', views.export_csv, name='export_csv'),
]