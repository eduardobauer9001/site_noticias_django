from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required # Novo import para restrição de acesso
from django.utils import timezone # Para converter string em data se necessário, ou use parse_datetime
from .models import Post, Comment, Category 
from .forms import PostForm, CommentForm # Importar CommentForm
from django.http import Http404 # Novo import para erro 404

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona o formulário de comentários vazio ao contexto
        context['comment_form'] = CommentForm() 
        return context

# NOVA VIEW FUNCIONAL: Lida com a submissão do formulário de comentários
@login_required # O usuário precisa estar logado para comentar
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Não salva no banco ainda (commit=False)
            comment = form.save(commit=False)
            comment.post = post          # Define o Post (chave estrangeira)
            comment.author = request.user # Define o Autor (usuário logado)
            comment.save()
            # Redireciona para o detalhe do post após o sucesso
            return redirect('post_detail', pk=post.pk)
    
    # Em caso de GET ou falha, apenas redireciona para a página de detalhes
    return redirect('post_detail', pk=post.pk)

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

# NOVAS CLASSES-BASED VIEWS PARA CATEGORIAS

class CategoryListView(ListView):
    """View para listar todas as categorias disponíveis."""
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    """
    View para listar posts de uma categoria específica.
    Reutiliza o template de listagem de posts.
    """
    model = Category
    template_name = 'blog/category_detail.html' # Nomeamos um novo template
    context_object_name = 'category' # O objeto principal no contexto é a categoria

    # Sobrescrevemos o método para também pegar os posts relacionados e injetar no contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Requisito: Listar todos os posts pertencentes a esta categoria (ordenado por data)
        context['posts'] = self.object.posts.all().order_by('-published_date')
        
        # O DetailView já trata o 404 automaticamente se o PK for inválido.
        # Não precisamos de lógica extra para o 404 aqui.
        return context