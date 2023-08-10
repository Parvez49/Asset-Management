from django.db import models

# Create your models here.

from django.contrib.auth.hashers import make_password
    

class Company(models.Model):
    name = models.CharField(max_length=100)
    registration_no=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.name

class UserData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.username
    

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    employee_id=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Device(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DeviceAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.device} assigned to {self.employee}"

class DeviceConditionLog(models.Model):
    device_assignment = models.ForeignKey(DeviceAssignment, on_delete=models.CASCADE)
    check_in_condition = models.TextField()
    check_out_condition = models.TextField()
    log_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.device_assignment}"
