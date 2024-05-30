"""
URL configuration for restoranapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from accounts.api.views import CustomerRegisterView,RestaurantRegisterView
from django.contrib.auth import views as auth_views

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('accounts.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
    path('dj-rest-auth/registration/customer', CustomerRegisterView.as_view(), name='customer_rest_register'),
    path('dj-rest-auth/registration/restoran', RestaurantRegisterView.as_view()),
    path('dj-rest-auth/password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token')
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)