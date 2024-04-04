from django.db import models
from django.contrib.auth.models import User


class EmployeeDetail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    empcode =  models.CharField(max_length=25,null=True)
    designation =  models.CharField(max_length=25,null=True)
    contact =  models.CharField(max_length=25,null=True)
    gender =  models.CharField(max_length=25,null=True)
    joiningdate =  models.DateField(max_length=25,null=True)

    def __str__(self):
        return self.user.username
    
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time_in = models.TimeField(null=True)
    time_out = models.TimeField(null=True)

 



