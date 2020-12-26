from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator

from .forms import PostForm, FormComments
from .models import Post, Group, User, Comment


def index(request):
    """Главная страницы"""
    posts = Post.objects.select_related("group")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator
    }
    return render(request, "index.html", context)


def group_posts(request, slug):
    """Страница автора"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "group": group,
        "page": page,
        "paginator": paginator
    }
    return render(request, "group.html", context)


def new_post(request):
    """Страница добовления поста"""

    if request.method != "POST":
        form = PostForm()
        context = {"form": form}
        return render(request, "new.html", context)

    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    context = {
        "form": form,
        "is_edit": False
    }
    return render(request, 'index.html', context)


def profile(request, username):
    # Профиль пользователя
    author_posts = get_object_or_404(User, username=username)
    posts = author_posts.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "author_posts": author_posts,
        "paginator": paginator
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    """Просмотр поста + комментарии"""
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    author_posts = post.author
    comments = post.comments.all()
    form = FormComments()
    context = {
        "author_posts": author_posts,
        "post": post,
        "form": form,
        "comments": comments
    }

    return render(request, "post.html", context)


def post_edit(request, username, post_id):
    # Страница редактирования поста
    post = get_object_or_404(Post, id=post_id)
    if request.user.username != username:
        return redirect("post", username=username, post_id=post_id)

    if request.method != "POST":
        form = PostForm(instance=post, files=request.FILES or None)
        context = {
            "form": form,
            "is_edit": True,
            "post": post,
        }
        return render(request, "post_new.html", context)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('post', username, post_id)
    context = {
        "form": form,
        "is_edit": True,
        "post": post,

    }
    return render(request, "post_new.html", context)


def add_comment(request, username, post_id):
    """Форма комментариев"""
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=request.user)

    if request.method != "POST":
        form = FormComments()
        context = {
            "form": form
        }
        return render(request, "includes/comments.html", context)

    form = FormComments(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = author
        comment.save()
        return redirect("post", username=username, post_id=post_id)


def page_not_found(request, exception):
    """Ошибка страницы"""
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Ошибка сервира"""
    return render(request, "misc/500.html", status=500)
