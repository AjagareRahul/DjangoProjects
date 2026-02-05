from django.shortcuts import render

# Create your views here.
def set_view(request):
    request.session['name']='Rahul'
    return render(request,'testapp/setsession.html')
def get_view(request):
    name=request.session.get('name')
    return render(request,'testapp/getssession.html',{'name':name})
   
def del_view(request):
    if 'name' in request.session: 
        del request.session['name']   
        
    return render(request, 'testapp/delsession.html')
