from django.shortcuts import render
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.

@api_view(['GET','POST'])
def get_employee(request):
    emp=Employee.objects.all()
    serializer=EmployeeSerializer(emp,many=True)
    return Response({'data':serializer.data})

class lIST_Employee(APIView):
    def get(self,request):
        emp=Employee.objects.all()
        serializer=EmployeeSerializer(emp,many=True)
        return Response({'data':serializer.data})
    
    def post(self,request):
        serializer_data=EmployeeSerializer(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            obj=serializer_data.save()
            return Response({'succes':"{}record inserted successfully".format(obj.name)})
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Details(APIView):
    def get(self,request,id):
        emp=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(emp)
        return Response({'data':serializer.data})
    
    def put(self,request,id):
        emp=Employee.objects.get(id=id)
        serializer_data=EmployeeSerializer(emp,data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            obj=serializer_data.save()
            return Response({'success':"{} record update successfully".format(obj.name)})
        return Response(serializer_data.error,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        emp=Employee.objects.get(id=id)
        emp.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

        