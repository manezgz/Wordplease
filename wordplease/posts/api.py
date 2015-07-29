from django.http import HttpResponse,HttpResponseNotFound, Http404
from datetime import datetime
from posts.models import Post
from django.contrib.auth.models import User
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer,PostDetailSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q


class PostListAPI(ListCreateAPIView):
   serializer_class = PostSerializer

   def get_queryset(self):
        blogname = self.kwargs.get('blogname',None)
        try:
            user=User.objects.get(username=blogname)
        except User.DoesNotExist:
            raise Http404("Blog does not exist")

        if not self.request.user.is_authenticated():
            posts= Post.objects.filter(owner=user, publication_date__lte=datetime.now())
        elif self.request.user.is_superuser:
            posts=Post.objects.filter(owner=user)
        else:
            posts=Post.objects.filter(owner=user).filter(Q(owner=self.request.user) | Q(publication_date__lte=datetime.now()))

        return posts

   def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailAPI(RetrieveUpdateDestroyAPIView):
   serializer_class = PostDetailSerializer
   permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

   def get_queryset(self):
        blogname = self.kwargs.get('blogname',None)
        try:
            user=User.objects.get(username=blogname)
        except User.DoesNotExist:
            raise Http404("Blog does not exist")
        return Post.objects.filter(owner=user)



