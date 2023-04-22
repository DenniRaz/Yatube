from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post
from .utils import pagination

User = get_user_model()

POSTS_PER_PAGE = 10


def index(request):
    """Главная страница."""
    posts = Post.objects.select_related('author', 'group')
    page_obj = pagination(request, posts, POSTS_PER_PAGE)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница группы."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.select_related('group')
    page_obj = pagination(request, posts, POSTS_PER_PAGE)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Страница пользователя."""
    author = get_object_or_404(User, username=username)
    posts = author.user_posts.select_related('author')
    page_obj = pagination(request, posts, POSTS_PER_PAGE)
    user = request.user
    following = (
            request.user != author
            and user.is_authenticated
            and Follow.objects.filter(
        user=request.user,
        author=author,
    ).exists()
    )
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Страница поста."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(
        request.POST or None,
        instance=post,
    )
    comments = post.comments.select_related('author')
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Страница создания поста."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author)


@login_required
def post_edit(request, post_id):
    """Страница редактирования поста."""
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id,
    }
    if request.user != post.author:
        return redirect('posts:posts_detail', post_id)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', context)
    form.save()
    return redirect('posts:posts_detail', post_id)


@login_required
def add_comment(request, post_id):
    """Добавление комментария к посту."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:posts_detail', post_id)


@login_required
def follow_index(request):
    """Страница подписок."""
    posts = Post.objects.filter(author__following__user=request.user)
    page_obj = pagination(request, posts, POSTS_PER_PAGE)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Подписка на автора."""
    user = get_object_or_404(User, username=username)
    if not Follow.objects.filter(
            user=request.user,
            author=user,
    ).exists() and (request.user != user):
        Follow.objects.create(user=request.user, author=user)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """Отписка от автора."""
    get_object_or_404(
        Follow,
        author__username=username,
        user=request.user,
    ).delete()
    return redirect('posts:profile', username=username)
