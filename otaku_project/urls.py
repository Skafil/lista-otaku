"""otaku_project URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from otaku_app.views import *
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    # Linki do aplikacji otaku_app.
    path('table_titles/', table_titles, name='table_titles'),
    path('table_category/<int:title_id>', table_category, 
        name='table_category'),
    path('table_subcategory/<int:category_id>/', table_subcategory,
        name="table_subcategory"),

    path('new_title/', new_title, name="new_title"),
    path('new_category/<int:title_id>', new_category, name="new_category"),
    path('new_subcategory/<int:category_id>/', new_subcategory,
        name='new_subcategory'),

    path('edit_title/<int:title_id>/', edit_title, name='edit_title'),
    path('edit_category/<int:category_id>/', edit_category, 
        name='edit_category'),
    path('edit_subcategory/<int:subcategory_id>/',edit_subcategory,
        name='edit_subcategory'),

    path('delete_title/<int:title_id>/', delete_title, name='delete_title'),
    path('delete_category/<int:category_id>/',delete_category, 
        name='delete_category'),
    path('delete_subcategory/<int:subcategory_id>/', delete_subcategory, 
        name='delete_subcategory'),

    # Linki do aplikacji users.
    path('register', RegistrationView.as_view(), name="register"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
        name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), 
        name='validate_email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('login', LoginView.as_view(), name="login"),
    path('logout', logout_view, name="logout_view"),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), 
        name='request-password'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(),
        name='reset-user-password'),
]
