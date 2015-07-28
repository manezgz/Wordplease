from django.http import HttpResponse,HttpResponseNotFound, Http404
from posts.models import Post
from django.contrib.auth.models import User
from posts.serializers import PostSerializer,PostDetailSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostListAPI(ListCreateAPIView):
   serializer_class = PostSerializer
   permission_classes = (IsAuthenticatedOrReadOnly,)

   def get_queryset(self):
        blogname = self.kwargs.get('blogname',None)
        try:
            user=User.objects.get(username=blogname)
        except User.DoesNotExist:
            raise Http404("Blog does not exist")
        #Me traigo el user para filtrar
        return Post.objects.filter(owner=user)

class PostDetailAPI(RetrieveUpdateDestroyAPIView):
   serializer_class = PostDetailSerializer

   def get_queryset(self):
        blogname = self.kwargs.get('blogname',None)
        try:
            user=User.objects.get(username=blogname)
        except User.DoesNotExist:
            raise Http404("Blog does not exist")
        return Post.objects.filter(owner=user)



