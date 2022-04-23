"""health_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path

from health import views
from health_world import settings

urlpatterns = [
    path('', views.home),
    path('refreshCaptcha/', views.refreshCaptcha),
    path('signup/', views.signup),
    path('signup_doctor/', views.signup_doctor),
    path('signup_doctor_ajax/', views.signup_doctor_ajax),
    path('signup2/', views.signup2),
    path('emailGeneration/', views.emailGeneration),
    path('emailValidation/', views.emailValidation),
    path('doctorEmailValidation/', views.doctorEmailValidation),
    path('login/patient/', views.user_login),
    path('login/patient/upload_document/', views.upload_document),
    path('login/patient/upload_document_2/<str:id>', views.upload_document_2),
    path('forgot_password/', views.forgot_password),
    path('forgot_password_otp/', views.forgot_password_otp),
    path('doctors_verification/',views.doctors_verification),
    path('logout/', views.logout),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
