from django.urls import path
from .views import RegisterView, VerifyEmail,LoginAPIView



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

]