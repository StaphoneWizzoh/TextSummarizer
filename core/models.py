from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Summary(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    input_file = models.FileField(upload_to="files/input/", default=None)
    generated_text = models.TextField(blank=True)
    generated_file = models.FileField( upload_to="files/generated/",default=None,blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Summaries"
