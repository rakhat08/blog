from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect


from .models import Article
from .forms import ArticleForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


@login_required(login_url='register')
def my_article_list(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'my_article_list.html', {'articles': articles})

def all_articles(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})

def full_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = CommentForm()
    if request.user.is_authenticated and request.user != article.author:
        article.views += 1
        article.save(update_fields=['views'])
    comments = article.comments.all()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Вы должны быть авторизованы, чтобы написать комментарий', extra_tags='danger')
            return redirect('full_article', pk=article.pk)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.author = request.user
                comment.save()
                return redirect('full_article', pk=article.pk)

    else:
        form = CommentForm()
    return render(request, 'full_article.html', {'article': article, 'comments': comments, 'form': form, 'views': article.views})

def create_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
        return redirect('my_article_list')
    return render(request, 'create_article.html', {'form': form} )

def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
        return redirect('my_article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'article': article, 'form': form})

def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('my_article_list')
    return render(request, 'delete_article.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user )
            return redirect('my_article_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('all_articles')
