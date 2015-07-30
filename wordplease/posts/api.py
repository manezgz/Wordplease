from django.http import HttpResponse,HttpResponseNotFound, Http404
from datetime import datetime
from posts.models import Post
from django.contrib.auth.models import User
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer,PostDetailSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        else:
            return PostDetailSerializer



    def get_queryset(self):
        blogname = self.kwargs.get('blogname',None)
        try:
            user = User.objects.get(username=blogname)
        except User.DoesNotExist:
            raise Http404("Blog does not exist")

        posts=Post.objects.filter(owner=user).order_by('-publication_date')

        if self.action == 'list':
            if not self.request.user.is_authenticated():
                posts = posts.filter(publication_date__lte=datetime.now())
            elif not self.request.user.is_superuser:
                posts = posts.filter(Q(owner=self.request.user) | Q(publication_date__lte=datetime.now()))

            #Comprobamos el titulo y el body
            titulo = self.request.query_params.get('titulo', None)
            if titulo is not None:
                posts=posts.filter(titulo__contains=titulo)

            contenido = self.request.query_params.get('contenido', None)
            if contenido is not None:
                posts=posts.filter(post_body__contains=contenido)

            #Por ultimo el orden si no los pasan
            orden = self.request.query_params.get('orden', None)
            if orden is not None:
                posts=posts.order_by(orden)

        return posts

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

