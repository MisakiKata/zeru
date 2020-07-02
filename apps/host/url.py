from django.urls import path
from apps.host import views


app_name = 'host'

extra_urlpatter = [
    path('host/', views.host, name='host'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit'),
    path('passwd/', views.passwd, name='passwd'),
]