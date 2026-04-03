from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Comment
from .forms import PostForm, CategoryForm, CommentForm


def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'post':
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('home')

        elif form_type == 'category':
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('home')

        elif form_type == 'comment':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('home')

    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    post_form = PostForm()
    category_form = CategoryForm()
    comment_form = CommentForm()

    return render(request, 'home.html', {
        'posts': posts,
        'categories': categories,
        'post_form': post_form,
        'category_form': category_form,
        'comment_form': comment_form,
    })


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('home')
    return render(request, 'delete_category.html', {'category': category})


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'delete_comment.html', {'comment': comment})
