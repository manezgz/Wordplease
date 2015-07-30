"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from posts.views import HomeView
from users.api import UserViewSet
from users.views import LoginView, SignupView
from blogs.api import BlogListAPI,BlogAPI
from posts.api import PostViewSet

post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$',HomeView.as_view(),name='home'),

    url(r'^blogs/$','posts.views.blogs', name='blogs_gral'),

    url(r'^new-post$','posts.views.newPost', name='new_post'),

    url(r'^blogs/(?P<username>\w{0,50})/$' , 'posts.views.blogposts', name='blog_user'),

    url(r'^blogs/(?P<username>\w{0,50})/(?P<postid>\d+)/$','posts.views.postDetail' , name='post_detail'),

    url(r'^login$', LoginView.as_view(), name='users_login'),

    url(r'^logout','users.views.logout', name='users_logout'),

    url(r'^signup', SignupView.as_view(), name='user_signup'),

    # Users API URLs
    url(r'^api/1.0/users/$',user_list, name='user_list_api'),

    url(r'^api/1.0/users/(?P<username>\w{0,50})/$',user_detail, name='user_list_api'),

    # Blogs API URLs
     url(r'^api/1.0/blogs/$',BlogListAPI.as_view(), name='blog_list_api'),

     url(r'^api/1.0/blogs/(?P<blogname>\w{0,50})$',BlogAPI.as_view(), name='blog_detail_api'),

    # Posts API URLs
    #url(r'',include(router.urls))

     url(r'^api/1.0/posts/(?P<blogname>\w{0,50})/$',post_list, name='post_list_api'),

     url(r'^api/1.0/posts/(?P<blogname>\w{0,50})/(?P<pk>\d+)/$',post_detail, name='post_detail_api')

]
