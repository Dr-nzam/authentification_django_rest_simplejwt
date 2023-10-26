from django.shortcuts import render
from rest_framework.views import APIView
from compte.models import CustomUser
from compte.sendmail import sendMail
from compte.serializer import UserSerializer
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password

from compte.serializers.inSerializers import ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


@api_view(['POST'])  
def reset_password_email(request):
        serializer = ResetPasswordEmailRequestSerializer(data=request.data)
        if serializer.is_valid():
            sendMail(serializer.data['email'])
            return Response({"detail": "email sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
def reset_password(request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            users = CustomUser.objects.filter(email=email)
            if not users.exists():
                return Response({"details":"Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            
            if users[0].otp !=otp:
                return Response({"details":"Wrong otp"}, status=status.HTTP_400_BAD_REQUEST)
            if  request.data["password"] != request.data['confirmPassword']:
                return Response({"detail": "Password do not match "}, status=status.HTTP_400_BAD_REQUEST)
            
            if  users[0].is_active != False:
                return Response({"detail": "Password do not match "}, status=status.HTTP_400_BAD_REQUEST)
           
            user:CustomUser = users.first()
            user.password = make_password(request.data["password"])
            user.is_active = True
            user.save()
            return Response({"detail": "password reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)