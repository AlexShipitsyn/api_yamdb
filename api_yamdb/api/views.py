from django.contrib.auth.tokens import default_token_generator as dtg
from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (
    ExistingRegistrationSerializer, NewRegistrationSerializer,
    TokenSerializer, UserSerializer, UserSelfSerializer)
from api.permissions import IsAdmin
from reviews.models import User


def send_mail(user):
    subject = 'Confirmation code'
    to = user.email
    text_content = f'Confirmation code: {dtg.make_token(user)}'
    mail.send_mail(subject, text_content, None, [to])


@api_view(['POST'])
@permission_classes([AllowAny])
def get_code(request):
    serializer = ExistingRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    if User.objects.filter(username=username, email=email).exists():
        send_mail(User.objects.get(username=username, email=email))
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = NewRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_mail(User.objects.get(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email']
    ))
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username'])
    if dtg.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserSelfSerializer
    )
    def user_own_profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Если намучались с PUT - вот решение:
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
