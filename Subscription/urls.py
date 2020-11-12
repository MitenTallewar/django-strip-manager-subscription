from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.conf import settings
from managerapp.views import RegisterUser,SignUp,email_verify

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signUp/',SignUp.as_view(),name='signUp'),
    path('isEmailExist/',email_verify,name='isEmailExist'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('users/',include('managerapp.urls')),
    path('admin/', admin.site.urls),
]
