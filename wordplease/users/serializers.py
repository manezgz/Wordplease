# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField() # read only
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        """
        Crea una instancia de User a partir de los datos de validated_data que contiene valores
        deserailizados
        :param validated_data:
        :return:
        """
        instance=User()
        return self.update(instance,validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza una instancia de User a partir de los datos de validated_data que contiene valores
        deserializados
        :param instance:
        :param validated_data:
        :return:
        """
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate_username(self,user_data):
        users=User.objects.filter(username=user_data)
        # Si estoy creando (no hay instancia) comprobar si hay usuarios con ese username
        if not self.instance and len(users) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese username")
        # Si estoy actualizando, el nuevo username es diferente al de la instancia (está cambiado el username)
        # y existen usuarios ya registrados con el nuevo username
        elif self.instance and self.instance.username != user_data and len(users) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese username")
        else:
            return user_data