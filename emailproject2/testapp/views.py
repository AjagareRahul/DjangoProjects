from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse


# Create your views here.
def send_test_email(request):
    subject="Welcome to my Blog"
    message="Thank you for visiting"
    from_email="ajagarerahul@gmail.com"
    recipient_list=["rajeecjadhav020@gmail.com"]
    send_mail(subject,message,from_email,recipient_list)
