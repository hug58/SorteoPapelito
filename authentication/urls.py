from django.urls import path
from .views import (     RegisterView, 
                         VerifyEmail,LoginAPIView, 
                         SetNewPasswordAPIView,
                         RequestPasswordResetEmail
                        )



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    #path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/<uidb64>/<token>/', SetNewPasswordAPIView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', RequestPasswordResetEmail.as_view(),name='password-reset-complete')
    
]
