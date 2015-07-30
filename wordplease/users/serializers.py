# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

   class Meta:
        model = User
        read_only_fields = ('id')
        write_only_fields = ('password',)
        fields = ('username', 'first_name', 'last_name','email','password')

   def validate_username(self, data):
        """
        Valida si existe un usuario con ese username
        """
        users = User.objects.filter(username=data)

        # Si estoy creando (no hay instancia) comprobar si hay usuarios con ese username
        if not self.instance and len(users) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese username")
        # Si estoy actualizando, el nuevo username es diferente al de la instancia (está cambiado el username)
        # y existen usuarios ya registrados con el nuevo username
        elif self.instance and self.instance.username != data and len(users) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese username")
        else:
            return data


class UserDetailSerializer(serializers.ModelSerializer):

     class Meta:
        model = User
        read_only_fields = ('id','username')
        fields = ('username', 'first_name', 'last_name','email')
