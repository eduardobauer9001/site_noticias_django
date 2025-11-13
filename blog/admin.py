from django.contrib import admin
from .models import Post, Comment # Importar Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')

# NOVO REGISTRO
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('text',)