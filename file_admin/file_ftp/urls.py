from django.contrib import admin
from django.urls import path

from file_ftp import views


urlpatterns = [

    path('ftp/', views.ftp),
    path('ftp_list/', views.ftp_list),
    path('admin_classify/', views.admin_classify),
    path('add_classify/', views.add_classify),
    path('readme/', views.readme),

]