from django.db import models

# Create your models here.
class Article(models.Model):
    judul = models.CharField("Judul", max_length=255, blank = True, null = True)
    jenis_penyakit = models.CharField(max_length=15, blank = True, null = True)
    isi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.judul