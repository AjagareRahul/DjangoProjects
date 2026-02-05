from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def send(request):
    if request.method=='POST':
        to=request.POST.get('txt1')
        msg=request.POST.get('txt2')
        send_mail("TestMail", msg, settings.EMAIL_HOST_USER, [to])
        return render(request,'testapp/home.html')
         #print("To:",to)
        #print("MSG:",msg)
    else:
        return render(request,'testapp/home.html')