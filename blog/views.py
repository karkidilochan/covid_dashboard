from django.shortcuts import get_object_or_404, redirect, render
from blog.models import BlogPost
from account.models import Account
from django.db.models import Q
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from django.http import HttpResponse

# Create your views here.


def create_blog_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
        return redirect('home')

    context['form'] = form

    return render(request, 'blog/create_blog.html', context)


def detail_blog_view(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse('You are not the author of the post')

    if request.POST:
        form = UpdateBlogPostForm(
            request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated'
            blog_post = obj

    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
        }
    )

    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    # example queries=hi there mister = [hi,there,mister]
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


def delete_view(request, slug):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)
    blog_post.delete()
    return redirect('home')
