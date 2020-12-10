from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator

from .forms import PostForm
from .models import Post, Group, User


def index(request):

    """Главная страницы"""
    post_list = Post.objects.select_related("group").order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page
    }
    return render(request, "index.html", context)


def group_posts(request, slug):
    """Страница автора"""
    group = get_object_or_404(Group, slug=slug)
    # post_list = Post.objects.select_related("group").order_by("-pub_date")
    author = Group.objects.get(slug=slug)
    post_list = author.posts.all().order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "group": group,
        "page": page
    }
    return render(request, "group.html", context)


def new_post(request):
    """Страница добовления поста"""

    if request.method != "POST":
        form = PostForm()
        context = {"form": form}
        return render(request, "new.html", context)

    form = PostForm(request.POST)
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

    author_posts = User.objects.get(username=username)
    posts = author_posts.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "author_posts": author_posts
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):

    author_posts = User.objects.get(username=username)
    number_post = Post.objects.get(id=post_id)
    context = {
        "author_posts": author_posts,
        "number_post": number_post
    }

    return render(request, 'post.html', context)


def post_edit(request, username, post_id):
    number_post = Post.objects.get(id=post_id)

    if request.user.username != username:
        return redirect("post", username=username, post_id=post_id)

    if request.method != "POST":
        form = PostForm(instance=number_post)
        context = {
            "form": form,
            "is_edit": True
        }
        return render(request, "post_new.html", context)

    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    context = {
        "form": form,
        "is_edit": True
    }
    return render(request, "post_new.html", context)
