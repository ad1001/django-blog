from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Story(models.Model):
    title = models.CharField(max_length = 150)
    content = models.TextField()
    meta = models.CharField(max_length = 250)
    view_count = models.IntegerField(default=0)
    ips = models.TextField(default = '')
    live_users = models.TextField(default='')
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'stories'
