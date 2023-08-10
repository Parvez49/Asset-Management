

from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


from rest_framework import serializers
from .models import Employee, Device

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import UserData

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['company', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserData(**validated_data)
        user.set_password(password)
        user.save()
        return user



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

from .models import DeviceAssignment

class DeviceAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceAssignment
        fields = '__all__'