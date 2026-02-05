from django.shortcuts import render
from testapp.models import Image
from testapp.form import UploadForm


# Create your views here.
def upload_img(request):
    if request.method=="POST":
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            #return render(request,'testapp/ulpoadimg.html',{'form':form})
        
    form= UploadForm() 
    img=Image.objects.all()
    return render(request,'testapp/ulpoadimg.html',{'img':img,'form':form})
