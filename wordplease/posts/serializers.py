from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        read_only_fields = ('id',)
        fields = ('id', 'titulo', 'resumen','urlImage','created_at','owner')


class PostDetailSerializer(PostSerializer):

    class Meta:
        model = Post
        read_only_fields = ('id',)
