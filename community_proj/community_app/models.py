from django.db import models
from django.utils import timezone

# Create your models here.

class Community(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='Community', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Community, on_delete = models.CASCADE)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.comment