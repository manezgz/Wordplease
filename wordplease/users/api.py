from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.pagination import PageNumberPagination
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from users.permissions import UserPermission


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (UserPermission,)
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        if self.action == 'list':
            user=User.objects.all();
        else:
            username = self.kwargs.get('username',None)
            try:
                user = User.objects.filter(username=username)
            except User.DoesNotExist:
                raise Http404("Blog does not exist")

        return user

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)