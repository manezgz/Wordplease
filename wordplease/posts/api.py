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

        if self.action == 'list':
            if not self.request.user.is_authenticated():
                posts = Post.objects.filter(owner=user, publication_date__lte=datetime.now())
            elif self.request.user.is_superuser:
                posts=Post.objects.filter(owner=user)
            else:
                posts=Post.objects.filter(owner=user).filter(Q(owner=self.request.user) | Q(publication_date__lte=datetime.now()))
        else:
            posts=Post.objects.filter(owner=user)

        return posts

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

