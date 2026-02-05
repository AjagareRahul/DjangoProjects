from django.shortcuts import render,redirect
from testapp.models import Image
from testapp.form import  ImageForm
# Create your views here.
def upload_img(request):
    if request.method=="POST":
        form=ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return redirect('show')
    form=ImageForm()
    return render(request,'testapp/uploadimg.html',{'form':form})
def show_img(request):
    images=Image.objects.all()
    return render(request,'testapp/show.html',{'images':images})
