from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from .models import *
def index(request):
    return render(request,'index.html')

def registration(request):
    error=""
    if(request.method=="POST"):
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        empcode=request.POST['empcode']
        email = request.POST['email']
        pwd = request.POST['password']
        try:
            user = User.objects.create_user(first_name=fn,last_name=ln,username=email,password=pwd)
            EmployeeDetail.objects.create(user= user,empcode=empcode)
            error="no"
        except:
            error="yes"
    return render(request,'registration.html',locals())



def emp_login(request):
    error = ""
    if( request.method=='POST'):
        e=request.POST['email']
        p=request.POST['password']
        user = authenticate(username=e,password=p)
        if user:
            login(request,user)
            # error("no")
            error = "no"
            
        else:
            error="yes"    

    return render(request,'emp_login.html',locals())

def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request,'emp_home.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error=""
    user=request.user
    employee=EmployeeDetail.objects.get(user=user)

    if(request.method=="POST"):
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        empcode=request.POST['empcode']
        email = request.POST['email']
        # department = request.POST['department']
        designation=request.POST['designation']
        joiningdate=request.POST['joiningdate']
        gender =request.POST['gender']
        contact=request.POST['contact']

        employee.user.first_name= fn
        employee.user.last_name=ln
        employee.empcode=empcode
        # employee.department = department
        employee.designation=designation
        employee.joiningdate=joiningdate
        employee.gender=gender
        employee.contact=contact

        if joiningdate:
            employee.joiningdate = joiningdate

        try:
            employee.save()
            employee.user.save()
            error="no"
        except:
            error="yes"
    return render(request,'profile.html',locals())



def Logout(request):
    logout(request)
    return redirect('index')