

from django.urls import path
from .views import *

urlpatterns = [
    path("add-company/",addCompany),
    path('create-user/', createUser),

    path('login/',loginUser),

    path('add-employee/', addEmployee),
    path('add-device/', addDevice),
    path('assign-device/', assignDevice),
]
