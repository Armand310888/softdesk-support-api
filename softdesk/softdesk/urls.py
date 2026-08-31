"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from rest_framework import routers

from projects.views import ProjectViewSet, ContributorViewSet
from users.views import UserViewSet

router = routers.SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include("rest_framework.urls")),
    path('api/', include(router.urls)),
    path(
        'api/projects/<int:project_pk>/contributors/',
        ContributorViewSet.as_view(
            {
                'get': 'list',
                'post': 'create'
            }
        ),
        name='list_contributors'
    ),
    path(
        'api/projects/<int:project_pk>/contributors/<int:pk>/',
        ContributorViewSet.as_view(
            {
                'delete': 'destroy'
            }
        ),
        name='delete_contributor'
    ),
]
