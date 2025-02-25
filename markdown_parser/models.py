from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    tags = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
