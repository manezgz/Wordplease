from django.db import models


class Categoria(models.Model):
    description = models.CharField(max_length=50,unique=True)