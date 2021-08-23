from rest_framework import generics, status, views
from .serializers import (  RegisterSerializer, 
                            EmailVerificationSerializer, 
                            LoginSerializer,
                            SetNewPasswordSerializer, 
                            ResetPasswordEmailRequestSerializer
)

from rest_framework.response import Response
from .models import User

from django.conf import settings

import jwt
import os

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import  force_str, smart_bytes



class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        current_site = get_current_site(request=request).domain
        relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        
        absurl = 'http://'+current_site + relativeLink
        email_body = f'Hello, \n Use link below to reset your password  \n {absurl}' 
        data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Create your passsword'}

        print(data)
        tasks = send_email.delay(data)
        print(tasks)
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        
        try:

            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])

            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        else:
            return Response('Email not found')
        
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        current_site = get_current_site(request=request).domain
        relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        
        absurl = 'http://'+current_site + relativeLink
        email_body = f'Hello, \n Use link below to reset your password  \n {absurl}' 
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your passsword'}

        send_email.delay(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)   
        password = request.data.get('password')

        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        if not user.is_verified:
            user.is_verified = True
            user.save()


        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response('The reset link is invalid',status=401)
        
        user.set_password(password)
        user.save()



        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

