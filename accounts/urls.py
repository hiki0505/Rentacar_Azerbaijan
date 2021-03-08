from django.urls import path, include
from .api import RegisterAPI, LoginAPI, RetrieveUpdateDestroyUserAPI, ListUserAPI, ValidatePhoneSendOTP, ValidateOTP, \
    UserDetail, ValidatePhoneForgot, ForgotValidateOTP, ForgetPasswordChange
from knox import views as knox_views

from rest_framework.routers import DefaultRouter

# from .api import UserAPI, LoginAPI

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/validate_phone', ValidatePhoneSendOTP.as_view(), name='send_otp'),
    # path('api/auth/validate_otp/<phone>', ValidateOTP.as_view(), name='validate_otp'),
    path('api/auth/validate_otp', ValidateOTP.as_view(), name='validate_otp'),
    path('api/auth/register', RegisterAPI.as_view(), name='register'),
    path('api/auth/forgot_info', ValidatePhoneForgot.as_view(), name='forgot-info'),
    path('api/auth/validate_forgot_otp', ForgotValidateOTP.as_view(), name='validate-forgot-otp'),
    path('api/auth/forgot_password_change', ForgetPasswordChange.as_view(), name='forgot-password-change'),
    # path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user/<int:pk>', RetrieveUpdateDestroyUserAPI.as_view(), name='user_detail'),
    path('api/auth/user', ListUserAPI.as_view(), name='user'),
    path('api/auth/user-info', UserDetail.as_view(), name='user-info'),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
]

# router = DefaultRouter()
# router.register('profile', UserAPI)
# router.register('login', LoginAPI, 'login')

# urlpatterns = router.urls
