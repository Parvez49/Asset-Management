from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company, Employee, UserData, Device, DeviceAssignment, DeviceConditionLog
from .serializers import CompanySerializer, EmployeeSerializer, UserDataSerializer, DeviceSerializer, DeviceAssignmentSerializer, DeviceConditionLogSerializer
from django.contrib.auth.hashers import check_password


import jwt
from rest_framework.exceptions import AuthenticationFailed
from jwt.exceptions import ExpiredSignatureError, DecodeError
import datetime
from django.utils import timezone

from django.db.models import Q

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'registration_no': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['name', 'registration_no']
    ),
    responses={
        200: openapi.Response('Company Added', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        401: openapi.Response('Unauthorized', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        403: openapi.Response('Forbidden', schema=openapi.Schema(type=openapi.TYPE_STRING)),
    }
)
@api_view(['POST'])
def addCompany(request):
    if request.method=="POST":
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Successfully added this company"})
        return Response(serializer.errors)



@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'company': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['company','username','email','password']
    ),
    responses={
        200: openapi.Response('User Added', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        401: openapi.Response('Unauthorized', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        403: openapi.Response('Forbidden', schema=openapi.Schema(type=openapi.TYPE_STRING)),
    }
)
@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"User created"}, status=201)
        return Response(serializer.errors, status=400)




@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'company': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['company','username','password']
    ),
    responses={
        200: openapi.Response('Successfully logged in..', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        401: openapi.Response('Unauthorized', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        403: openapi.Response('Forbidden', schema=openapi.Schema(type=openapi.TYPE_STRING)),
    }
)
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

@api_view(['GET'])
def logoutUser(request):
    response = Response()
    response.delete_cookie('logintoken')
    response.data = {"you are logged out"}
    return response



def authenticateUser(token):
    if not token:
        #return Response("Loggin first")
        raise AuthenticationFailed({"error":'Log in first!'})
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except ExpiredSignatureError:
        raise AuthenticationFailed({"error":'You session has expired!'})
    except DecodeError:
        raise AuthenticationFailed({"error":'Log in failed!'})
    return payload



@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'employee_id': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['name','employee_id']
    ),
    responses={
        200: openapi.Response('Employee Added', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        401: openapi.Response('Unauthorized', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        403: openapi.Response('Forbidden', schema=openapi.Schema(type=openapi.TYPE_STRING)),
    }
)
@api_view(['POST'])
def addEmployee(request):
    if request.method=='POST':
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        request.data['company']=payload['company']

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Successfully added"}, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def employeeList(request):
    if request.method=="GET":
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        # show all employees of company
        data=Employee.objects.filter(company=payload['company'])
        serializer=EmployeeSerializer(data,many=True)
        return Response(serializer.data)




@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'serial_no': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['name','serial_no']
    ),
    responses={
        200: openapi.Response('Device Added', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        401: openapi.Response('Unauthorized', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        403: openapi.Response('Forbidden', schema=openapi.Schema(type=openapi.TYPE_STRING)),
    }
)
@api_view(['POST'])
def addDevice(request):
    if request.method == 'POST':
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        request.data['company']=payload['company']
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Successfully added"}, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def deviceList(request):
    if request.method=="GET":
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        # show all devices
        data=Device.objects.filter(company=payload['company'])
        serializer=DeviceSerializer(data,many=True)
        return Response(serializer.data)




@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'employee_id': openapi.Schema(type=openapi.TYPE_STRING),
            'device_serial': openapi.Schema(type=openapi.TYPE_STRING),
            'assigned_date': openapi.Schema(type=openapi.TYPE_STRING),
            'return_date': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['employee_id','device_serial','assigned_date','return_date']
    ),
    responses={
        200: openapi.Response('Device Assigned', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        401: openapi.Response('Unauthorized', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        403: openapi.Response('Forbidden', schema=openapi.Schema(type=openapi.TYPE_STRING)),
    }
)
@api_view(['POST'])
def assignDevice(request):
    if request.method == 'POST':
        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        request.data['company']=payload['company']

        # Check if the employee exists
        employee=Employee.objects.filter(employee_id=request.data['employee_id'],company=payload['company']).first()
        if not employee:
            return Response({"error":"Employee not found"})
        
        # Check if the device exists
        device=Device.objects.filter(serial_no=request.data['device_serial'],company=payload['company']).first()
        if not device:
            return Response({"error": "Device not found"})
        
        device_id=device.pk
        if DeviceAssignment.objects.filter(device=device_id, return_date__gt=request.data['assigned_date']).exists():
            return Response({"error": "Device already assigned to another employee"}, status=400)

        last_assignment = DeviceAssignment.objects.filter(device_id=device_id).order_by('-return_date').first()
        if last_assignment:
            last_log=DeviceConditionLog.objects.filter(device_assignment=last_assignment.pk).first()

            # Check if the device damaged
            if last_log.check_out_condition=='bad':
                return Response({"error":"Device Damaged!"})
            condition=last_log.check_out_condition
            print(condition)
        else:
            condition='better'


        request.data['employee']=employee.pk
        request.data['device']=device.pk
        serializer = DeviceAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            obj=serializer.save()
            # Update the device codition log with the return date
            log=DeviceConditionLog(device_assignment=obj,check_in_condition=condition,check_out_condition="")
            log.save()
            return Response({"success":"Assigned device"}, status=201)
        return Response(serializer.errors, status=400)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'employee_id': openapi.Schema(type=openapi.TYPE_STRING),
            'device_serial': openapi.Schema(type=openapi.TYPE_STRING),
            'condition': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['employee_id','device_serial','condition']
    ),
    responses={
        200: openapi.Response('Device Returned', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        401: openapi.Response('Unauthorized', schema=openapi.Schema(type=openapi.TYPE_STRING)),
        403: openapi.Response('Forbidden', schema=openapi.Schema(type=openapi.TYPE_STRING)),
    }
)
@api_view(['POST'])
def returnDevice(request):
    if request.method == 'POST':

        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        #request.data['company']=payload['company']

        # Check if the employee exists
        employee=Employee.objects.filter(employee_id=request.data['employee_id'],company=payload['company']).first()
        if not employee:
            return Response({"error":"Employee not found"})
        
        # Check if the device exists
        device=Device.objects.filter(serial_no=request.data['device_serial'],company=payload['company']).first()
        if not device:
            return Response({"error": "Device not found"})


        # Check if the device is assigned to the given employee
        device_assignment = DeviceAssignment.objects.filter(employee=employee.pk,device=device.pk).first()

        if not device_assignment:
            return Response({"error": "Device is not assigned to the employee"}, status=400)


        device_condition_log=DeviceConditionLog.objects.filter(device_assignment=device_assignment).first()
        device_condition_log.check_out_condition=request.data['condition']
        device_condition_log.save()

        # Update the device assignment with the return date
        device_assignment.return_date = timezone.now().date()
        device_assignment.save()

        return Response({"message": "Device returned successfully"}, status=200)



@api_view(['GET'])
def assignmentList(request):
    if request.method == 'GET':
        # Retrieve the list of active (not returned) DeviceAssignment instances
        active_assignments = DeviceAssignment.objects.filter(return_date__gt=timezone.now().date())
        serializer = DeviceAssignmentSerializer(active_assignments, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def availableDevice(request):
    token=request.COOKIES.get("logintoken")
    payload=authenticateUser(token)

    filtered_assignments = DeviceAssignment.objects.filter(
            Q(return_date__lt=timezone.now()) | Q(deviceconditionlog__check_out_condition__icontains="bad")
        )

    # Retrieve the list of available devices
    available_devices = Device.objects.filter(company=payload['company']).exclude(
        deviceassignment__in=filtered_assignments
    )
    serializer = DeviceSerializer(available_devices, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def deviceLog(request):
    if request.method == 'GET':

        token=request.COOKIES.get("logintoken")
        payload=authenticateUser(token)

        # Retrieve the list of device condition logs
        device_logs = DeviceConditionLog.objects.filter(
            device_assignment__device__company=payload['company']
        )
        serializer = DeviceConditionLogSerializer(device_logs, many=True)
        return Response(serializer.data)





