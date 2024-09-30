from django.urls import path
from .views import SignUpAPI, SignInAPI, ForgotPasswordAPI

urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='signup'),
    path('signin/', SignInAPI.as_view(), name='signin'),
    #path('forgot-password/', ForgotPasswordAPI.as_view(), name='forgot-password'),
]
