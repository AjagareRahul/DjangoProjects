from django.shortcuts import render

# Create your views here.
def index(request):
    people=[
        {'name':'Rahul','sirname':'Ajagare','age':25},
        {'name':'Rajeev','sirname':'Jadhav','age':26},
        {'name':'Ravindar','sirname':'Soni','age':27}
    ]
    text='''    Lorem ipsum, dolor sit amet consectetur adipisicing elit. Aperiam voluptates similique id! Quasi doloremque commodi expedita quibusdam nesciunt suscipit eligendi cupiditate, nemo magnam quas earum ad officiis culpa obcaecati eius!
'''
    return render(request,'index.html',context={'data':people,'text':text})

