from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.utils import timezone # Para converter string em data se necessário, ou use parse_datetime
from .forms import PostForm # Podemos reutilizar o form da versão 2 ou deixar o django gerar

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # O DetailView já implementa o 404 automaticamente se não achar o ID

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm # Opcional: se tirar isso e por fields=['...'], funciona igual
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # success_url não é necessário se o model tiver o método get_absolute_url

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')