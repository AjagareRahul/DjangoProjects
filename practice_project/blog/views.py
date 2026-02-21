from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostForm
# Create your views here.
def post_list(request):
    post=Post.objects.all()
    return render(request,'blog_list.html',{'posts':post})
def post_details(request,id):
    post=get_object_or_404(Post,id=id)
    return render(request,'post_details.html',{'post':post})
def create_post(request):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        Post.objects.create(title=title,content=content)
        
        return redirect('post_list')
    return render(request,'create_post.html')
def update_post(request,id):
    post=get_object_or_404(Post,id=id)
    if request.method=='POST':
        post.title=request.POST.get('title')
        post.content=request.POST.get('content')
        post.save()
        return redirect('post_details',id=id)
    return render(request,'update_post.html',{'post':post})

def delete_post(request,id):
    post=get_object_or_404(Post,id=id)
    if request.method=='POST':
        post.delete()
        return redirect('post_list')
    return render(request,'delete_post.html',{'post':post})
def create_form_post(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form=PostForm()
    return render(request,'create_form_post.html',{'form':form})