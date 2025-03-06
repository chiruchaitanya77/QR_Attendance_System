"""
URL configuration for DjangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from QRcode import views as us

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', us.index),
    path('exit', us.exit),
    path('adminlogin', us.adminlogin),
    path('adminhome',us.adminhome),
    path('userRegister', us.userRegister),
    path('userhome', us.userhome),
    path('userlogin', us.userlogin),
    path('students/', us.students, name='students'),
    path('presents', us.presents, name='presents'),
    path('absents', us.absents, name='absents'),
    path('classes/', us.classes, name='classes'),
    path('activateuser/' ,us.activateuser, name='activateuser'),
    path('deactivateuser/' ,us.deactivateuser, name='deactivateuser'),
    path('deleteuser/' ,us.deleteuser, name='deleteuser'),
    path('otp/' ,us.otp, name='otp'),
    path('qrcodeimg/', us.qrcodeimg, name='qrcodeimg'),
    path('QRattendance/', us.QRattendance, name='QRattendance'),
    path('idcard/', us.idcard),
    path('google_auth/', us.google_auth, name='google_auth'),
    path('oauth2callback/', us.oauth2callback, name='oauth2callback'),
    path('update_google_sheet/', us.update_google_sheet, name='update_google_sheet'),
    path('download_sheet/', us.download_sheet, name='download_sheet'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
