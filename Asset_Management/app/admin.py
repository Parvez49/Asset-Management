from django.contrib import admin

# Register your models here.


from .models import Company, UserData, Employee, Device, DeviceAssignment, DeviceConditionLog

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Device)
admin.site.register(DeviceAssignment)
admin.site.register(DeviceConditionLog)
admin.site.register(UserData)
