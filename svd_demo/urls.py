from django.urls import path, re_path
from . import views

app_name = 'svd_demo'

urlpatterns = [
    path('', views.home, name='home'),
    path('compress/', views.compress, name='compress'),
    path('denoise/', views.denoise, name='denoise'),
    re_path(r'^result_compre/(?P<image_ids>[\d\-]+)/$', views.result_compre, name='result_compre'),
    re_path(r'^result_denoise/(?P<image_ids>[\d\-]+)/$', views.result_denoise, name='result_denoise'),
]
