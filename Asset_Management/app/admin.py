from django.contrib import admin

# Register your models here.


from .models import Company, UserData, Employee, Device, DeviceAssignment, DeviceConditionLog


admin.site.register(Company)

class UserDataAttr(admin.ModelAdmin):
    list_display=['company','username','email']
admin.site.register(UserData,UserDataAttr)

class EmployeeAttr(admin.ModelAdmin):
    list_display=['company','name','employee_id']
admin.site.register(Employee,EmployeeAttr)

class DeviceAttr(admin.ModelAdmin):
    list_display=['company','name','serial_no']
admin.site.register(Device,DeviceAttr)

class DeviceAssignmentAttr(admin.ModelAdmin):
    list_display=['employee','device','assigned_date','return_date']
admin.site.register(DeviceAssignment,DeviceAssignmentAttr)


admin.site.register(DeviceConditionLog)

