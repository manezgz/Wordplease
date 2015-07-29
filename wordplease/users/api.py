from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from users.permissions import UserPermission

class UserViewSet(GenericViewSet):

    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = UserPermission

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user=serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,username):
        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)  # compruebo si el usuario autenticado puede hacer GET en este user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self,request,username):
        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(instance=user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,username):
        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

