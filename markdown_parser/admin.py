from django.contrib import admin
from .models import Article

# Register your models here.
@admin.register(Article)
class ArticleADmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'tags')
    prepopulated_fields = {'slug': ('title',)}
