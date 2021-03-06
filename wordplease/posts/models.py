from categorias.models import Categoria
from django.db import models
from django.contrib.auth.models import User
from posts.settings import CATEGORIES

class Post(models.Model):
    owner=models.ForeignKey(User)
    titulo=models.CharField(max_length=80)
    resumen=models.CharField(max_length=500)
    post_body=models.CharField(max_length=2048,default="")
    urlImage=models.URLField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    categorias= models.ManyToManyField(Categoria)
    publication_date=models.DateField()