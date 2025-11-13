from django.db import models
from django.urls import reverse
from django.conf import settings # Necessário para referenciar o User model


# NOVO MODELO
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    description = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

    # Útil para o reverse de DetailView
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(verbose_name="Conteúdo (HTML)")
    published_date = models.DateTimeField(verbose_name="Data de Publicação")
    
    # NOVO CAMPO: Relação Muitos-Para-Muitos com Category
    categories = models.ManyToManyField(
        Category, 
        related_name='posts', # Permite acessar posts de uma categoria via category.posts.all()
        verbose_name="Categorias"
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    # Relacionamento: O comentário pertence a um Post. 
    # models.CASCADE garante que ao deletar o Post, os comentários também são deletados.
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='comments' # Permite acessar todos os comentários de um post via post.comments.all()
    )
    
    # O autor referencia o modelo User do Django
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Referência segura ao modelo User
        on_delete=models.CASCADE,
        verbose_name="Autor"
    )
    
    text = models.TextField(verbose_name="Comentário")
    
    # DateTimeField para a data de postagem (auto_now_add=True define a data automaticamente na criação)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Data de Postagem")

    class Meta:
        # Requisito: Exibir os comentários ordenados pelo mais recente primeiro
        ordering = ['-created_date'] 

    def __str__(self):
        return f"Comentário de {self.author.username} em {self.post.title[:20]}..."

