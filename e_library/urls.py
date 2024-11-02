"""
URL configuration for e_library project.

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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    ##path('users/', include('users.urls')),
    ##path('books/', include('books.urls')),
    ##path('borrowing/', include('borrowing.urls')),
    ##path('notifications/', include('notifications.urls')),
    path('user_auth/', include('user_auth.urls')) 
]
# schema_view = get_schema_view(
#    openapi.Info(
#       title="e_library",
#       default_version='v1',
#       description="Description of your API",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@yourapi.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#     # Your other URLs...
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('openapi/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
# ]
