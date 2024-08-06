from django.core.mail import send_mail
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status, authentication, filters
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from accounts.pagination import CustomPagination
from accounts.serializers import *
from rest_framework.response import Response
from pramogh import settings
import random


# Create your views here.
class RegistrationAPI(GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            payload = request.data.copy()
            payload['created_by'] = user['user']
            payload['updated_by'] = user['user']
            serializer = ProfileSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(user)
            return Response(serializer.errors)
        return Response(serializer.errors)


class UserLoginAPI(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get or Generate token
        token, created = Token.objects.get_or_create(
            user=serializer.validated_data['user'])
        request = {
            'user': serializer.validated_data['user']
        }
        response_serializer = UserLoginReplySerializer(token, context={'request': request})
        return Response(response_serializer.data)


class AccountDeleteView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDeleteSerializer

    def post(self, request):
        disable = request.data.get('disable', False)
        if disable:
            query = User.objects.filter(id=request.user.id).update(is_active=False)
            ctx = {
                'message': 'Account deleted successfully.'
            }
            return Response(ctx)
        query = User.objects.filter(id=request.user.id).delete()
        ctx = {
            'message': 'Account deleted successfully.'
        }
        return Response(ctx)


class PasswordChangeAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        password = request.data.get("password")
        confirmPassword = request.data.get("confirmPassword")

        if password != confirmPassword:
            return Response({'error': 'Password does not match'},
                            status=500)

        user = User.objects.get(pk=request.user.pk)
        user.set_password(password)
        user.save()
        return Response({'ok': 'Password changed successfully! '},
                        status=200)


class OTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = User.objects.filter(email=request.data['email']).last()
        if user:
            otp = random.randint(1111, 9999)
            try:
                subject = 'Kodehash'
                message = f'Hi {user.username}, Here is OTP from Kodehash.\n{otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                print('send email.')
            model_data = request.data.copy()
            model_data['otp'] = otp
            model_data['created_by'] = user.pk
            model_data['updated_by'] = user.pk
            serializer = OTPSerializer(data=model_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({'message': 'There is no user register with this email.'})

    def put(self, request):
        user = User.objects.filter(email=request.data['email']).last()
        if user:
            query_otp = Otp.objects.filter(user=user.id).last()
            if query_otp:
                query_data = {
                    'verify': 'true'
                }
                if int(request.data['otp']) == int(query_otp.otp):
                    query_update = OTPSerializer(query_otp, data=query_data)
                    if query_update.is_valid():
                        query_update.save()
                        return Response({'message': 'you have successfully verify OTP.'}, status=status.HTTP_200_OK)
                    return Response({'message': query_update.errors}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'OTP that you enter is not valid.', 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Please send OTP first.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'There is no user register with this email.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)

    def put(self, request):
        user = User.objects.filter(email=request.data['email']).last()
        if user:
            query_otp = Otp.objects.filter(created_by=user.id, verify='true').last()
            if query_otp:
                user.set_password(request.data['password'])
                user.save()
                # remove previous otp
                inst = Otp.objects.filter(created_by=user).delete()
                return Response({'message': 'You have successfully reset your password.'}, status=status.HTTP_200_OK)
            return Response({'message': 'First Verify OTP then reset your password'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'There is no user register with this email.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (authentication.TokenAuthentication,)
    pagination_class = CustomPagination

    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # search_fields = ['name', 'address']
    # filterset_fields = ['status', 'created_by']

    def list(self, request, *args, **kwargs):
        """Called when listing all objects"""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProfileDetailedSerializer
        return ProfileSerializer

    def get_queryset(self):
        filter_params = self.request.GET.dict()
        if 'page' in filter_params.keys():
            del filter_params['page']
        if filter_params:
            queryset = Profile.objects.filter(**filter_params).exclude(created_by=self.request.user)
        else:
            queryset = Profile.objects.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
