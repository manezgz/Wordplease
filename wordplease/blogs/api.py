from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from blogs.serializers import BlogSerializer
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import status
from django.db import connection
from blogs.models import Blog
from posts.models import Post

class BlogListAPI(APIView):

    def get(self, request):
        cursor=connection.cursor()
        cursor.execute("SELECT DISTINCT owner_id FROM posts_post")
        ids=cursor.fetchall();
        s1 = list();
        for id in ids:
            strId=str(id)
            strId=strId.replace(",","")
            strId=strId.replace("(","")
            strId=strId.replace(")","")
            s1.append(strId)
        users=User.objects.filter(pk__in=s1).order_by('username')
        blogs= list()
        #Recorro lista de users y creo un obj blog para cada uno y lo meto en una lista
        for user in users:
            blog = Blog(blog_name=user.username)
            blogs.append(blog)
        serializer = BlogSerializer(blogs, many=True)
        serialized_blogs= serializer.data
        return Response(serialized_blogs)

class BlogAPI(APIView):

    def get(self, request,blogname):
        user = get_object_or_404(User, username=blogname)
        #Miro si tiene algun post
        posts=get_list_or_404(Post,owner=user)
        blog = Blog(blog_name=user.username)
        serializer = BlogSerializer(blog)
        serialized_blogs= serializer.data
        return Response(serialized_blogs)