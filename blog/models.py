from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(verbose_name="Conteúdo (HTML)")
    published_date = models.DateTimeField(verbose_name="Data de Publicação")

    def __str__(self):
        return self.title
    
    # Útil para o redirect nas Class Based Views (Versão 3)
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
