from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('get_items/', ItemViewAPI.as_view()),
    path('post_items/', ItemViewAPI.as_view()),
    path('put_update_items/', ItemViewAPI.as_view()),
    path('patch_get_items/', ItemViewAPI.as_view()),
    path('delete_items/', ItemViewAPI.as_view()),
    path('healthcheck/', healthcheck, name='healthcheck'),
]
