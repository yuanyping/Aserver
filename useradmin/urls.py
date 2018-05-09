from django.urls import path
from  useradmin import  views
urlpatterns = [
    path('add_user/',views.add_user ),
    path('update_user/',views.update_user ),
    path('user_list/',views.user_list ),

]
