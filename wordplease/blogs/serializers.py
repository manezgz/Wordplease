from rest_framework import serializers
from django.contrib.auth.models import User


class BlogSerializer(serializers.Serializer):

    blog_name = serializers.CharField()
    blog_url = serializers.CharField()
