"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from file_ftp import views
from django.http import FileResponse
import platform

def down(request):
    file_path=request.GET.get("file")
    system_version=platform.system()
    print(file_path)
    if system_version == "Windows":
        file_name=file_path.split("\\")[3]
    elif system_version == "Linux":
        file_name = file_path.split("/")[3]
    else:
        file_name="test.tar"
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' %(file_name)
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('loginout/', views.loginout),
    path('file_admin/', include("file_ftp.urls")),
    path('down/', down),
    path('user_admin/', include("useradmin.urls")),
    re_path("^$", views.login),

]
