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
    path('login/', views.home),
    path('refreshCaptcha/', views.refreshCaptcha),
    path('signup/', views.signup),
    path('signup_doctor/', views.signup_doctor),
    path('signup_doctor_ajax/', views.signup_doctor_ajax),
    path('signup2/', views.signup2),
    path('emailGeneration/', views.emailGeneration),
    path('emailValidation/', views.emailValidation),
    path('doctorEmailValidation/', views.doctorEmailValidation),
    path('forgot_password/', views.forgot_password),
    path('forgot_password_otp/', views.forgot_password_otp),
    path('doctors_verification/', views.doctors_verification),
    path('doctors_verification/<str:id>', views.doctors_verification_completed),
    # user
    path('login/patient/', views.user_login),
    path('login/patient/upload_document/', views.upload_document),
    path('login/patient/upload_document_2/<str:id>', views.upload_document_2),
    path('login/patient/view_document/', views.view_document),
    path('login/patient/view_document/<str:id>', views.view_document_2),
    path('login/patient/edit_document/<str:id>', views.edit_document),
    path('login/patient/delete_document/<str:id>', views.delete_document),
    # tech
    path('login/technical/', views.technical),
    path('login/technical/backup/', views.get_backup),
    # doctor
    path('login/doctor/', views.doctor),
    path('login/doctor/phr_address/', views.phr_address),
    path('login/doctor/health_id/', views.health_id),
    path('login/doctor/view_user_document/<str:id>', views.view_user_document),

    path('logout/', views.logout),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
