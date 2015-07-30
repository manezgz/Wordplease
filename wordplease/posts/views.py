# -*- coding: utf-8 -*-
from categorias.models import Categoria

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.db import connection
from django.shortcuts import render
from posts.models import Post
from django.contrib.auth.models import User
from posts.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomeView(View):

    def get(self,request):
        posts=Post.objects.all().select_related('owner').order_by('-publication_date')
        posts=posts.filter(publication_date__lte=datetime.now())
        context=createPaginatedContextFromPostsList(request,posts)
        return render(request,'posts/home.html',context)

def createPaginatedContextFromPostsList(request,posts):
    paginator = Paginator(posts,9)
    page = request.GET.get('page')
    try:
        postsPaginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        postsPaginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        postsPaginated = paginator.page(paginator.num_pages)
    context={
        'posts_list':postsPaginated
    }
    return context



def blogs(request):
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
    users=User.objects.filter(pk__in=s1)
    context={
        'blogs_list':users
    }
    return render(request,'posts/blogs.html',context)

def blogposts(request,username):
    #Sacamos el id del usuario
    user=User.objects.filter(username=username)
    posts=Post.objects.all().select_related('owner').order_by('-publication_date')
    posts=posts.filter(publication_date__lte=datetime.now(),owner=user)
    context=createPaginatedContextFromPostsList(request,posts)
    return render(request,'posts/home.html',context)

def postDetail(request,username,postid):
    #Sacamos el id del usuario
    user=User.objects.filter(username=username)

    possible_post=Post.objects.filter(owner=user).filter(pk=postid)
    post=possible_post if len(possible_post)>=1 else None
    if post is not None:
        #cargamos los posts
        context={
            'posts_list':post
        }
        return render(request,'posts/post.html',context)
    else:
        return HttpResponseNotFound() #404 NotFound

@login_required()
def newPost(request):
   """

   :param request:
   :return:
   """
   success_message=''
   categorias =Categoria.objects.all()
   if request.method == 'GET':
       form=PostForm()
   else:
       post_with_owner = Post()
       post_with_owner.owner=request.user
       form=PostForm(request.POST,instance=post_with_owner)
       if form.is_valid():
           new_post=form.save()
           username=new_post.owner
           postid=new_post.pk
           success_message = 'Guardado con éxito'
           success_message += '<a href="{0}">'.format(reverse('post_detail',kwargs={'username':username,'postid':postid}))
           success_message += 'Ver Post'
           success_message += '</a>'
           form = PostForm()
   context = {
       'form' : form,
       'categorias' : categorias,
       'success_message' : success_message
   }
   return render(request, 'posts/new-post.html',context)
