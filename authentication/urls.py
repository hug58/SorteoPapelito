from django.urls import path
from .views import RegisterView, VerifyEmail, RequestPasswordResetEmail
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('register', RegisterView.as_view(), name="register"),


    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

]