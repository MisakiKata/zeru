"""zerus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from apps.host import views
from apps.logcat import urls
from apps.host import url
from apps.host.views import page_error, page_not_found
from apps.threat import urls as threat
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('logcat/', include(urls.extra_urlpatter)),
    path('host/', include(url.extra_urlpatter)),
    path('file/', include(threat.extra_urlpatter)),
    re_path(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
]
handler404 = 'apps.host.views.page_not_found'
handler500 = 'apps.host.views.page_error'