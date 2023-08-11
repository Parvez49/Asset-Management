

from django.urls import path
from .views import *

urlpatterns = [
    path("add-company/",addCompany),
    path('create-user/', createUser),

    path('login/',loginUser),
    path('logout/',logoutUser),

    path('add-employee/', addEmployee),
    path('employee-list/',employeeList),
    path('add-device/', addDevice),
    path('device-list/',deviceList),
    path('assign-device/', assignDevice),
    path('return-device/', returnDevice),

    path('device-assignments-list/', assignmentList),
    path('available-device/',availableDevice),
    path('device-logs/',deviceLog),
]
