from django.db import models

# Create your models here.
class Blog(object):
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.blog_url = 'http://localhost:8000/blogs/' + blog_name + ''