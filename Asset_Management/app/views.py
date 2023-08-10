from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company, Employee, UserData, Device, DeviceAssignment, DeviceConditionLog
from .serializers import CompanySerializer, EmployeeSerializer, UserDataSerializer, DeviceSerializer, DeviceAssignmentSerializer
from django.contrib.auth.hashers import check_password


import jwt
from rest_framework.exceptions import AuthenticationFailed
from jwt.exceptions import ExpiredSignatureError, DecodeError
import datetime


@api_view(['POST','GET'])
def addCompany(request):
    if request.method=="POST":
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method=="GET":
        data=Company.objects.all()
        serializer=CompanySerializer(data,many=True)
        return Response(serializer.data)


@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def loginUser(request):
    company=request.data['company']
    username=request.data['username']
    password=request.data['password']
    user = UserData.objects.filter(company=company,username=username).first()

    if not user:
        raise AuthenticationFailed('User not found!')

    if not check_password(password,user.password):
        raise AuthenticationFailed('Incorrect password!')    
     
    payload = {
        'id': user.id,
        'company':company,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()
    response.set_cookie(key='logintoken', value=token, httponly=True)
    response.data = {"You are logged in"}
    return response





def authenticateUser(token):
    if not token:
        return Response("Loggin first")
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except ExpiredSignatureError:
        raise AuthenticationFailed({"error":'You session has expired!'})
    except DecodeError:
        raise AuthenticationFailed({"error":'Log in failed!'})
    return payload




@api_view(['POST','GET'])
def addEmployee(request):
    if request.method=='POST':
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        request.data['company']=payload['company']

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method=="GET":
        data=Employee.objects.all()
        serializer=EmployeeSerializer(data,many=True)
        return Response(serializer.data)



@api_view(['POST'])
def addDevice(request):
    if request.method == 'POST':
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        request.data['company']=payload['company']
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    



@api_view(['POST'])
def assignDevice(request):
    if request.method == 'POST':
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        request.data['company']=payload['company']

        employee=Employee.objects.filter(employee_id=request.data['employee_id']).first()
        if not employee:
            return Response({"error":"Employee not found"})
        
        device=Device.objects.filter(serial_no=request.data['device_serial']).first()
        if not device:
            return Response({"error": "Device not found"})
        
        device_id=device.pk
        if DeviceAssignment.objects.filter(device=device_id, return_date__gt=request.data['assigned_date']).exists():
            return Response({"error": "Device already assigned to another employee"}, status=400)

        request.data['employee']=employee.pk
        request.data['device']=device.pk
        serializer = DeviceAssignmentSerializer(data=request.data)
        
        if serializer.is_valid():

            last_assignment = DeviceAssignment.objects.filter(device_id=device_id).order_by('-return_date').first()
            if last_assignment:
                last_log=DeviceConditionLog.objects.filter(device_assignment=last_assignment.pk).first()
                condition=last_log.check_out_condition
                print(condition)
            else:
                condition='better'

            obj=serializer.save()
            log=DeviceConditionLog(device_assignment=obj,check_in_condition=condition,check_out_condition="")
            log.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    











