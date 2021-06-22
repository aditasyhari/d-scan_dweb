from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    judul = models.CharField("Judul", max_length=255, blank = True, null = True)
    jenis_penyakit = models.CharField(max_length=15, blank = True, null = True)
    isi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.judul

# class Profile(models.Model):
#     user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     mobile = models.CharField(max_length=20)
#     otp = models.CharField(max_length=6)