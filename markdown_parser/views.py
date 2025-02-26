from django.shortcuts import render
from django.views.generic import ListView

from .models import Article

# Create your views here.
class ArticleListView(ListView):
    model = Article
    context_object_name = 'my_objects'
    template_name  = "article_list.html"
