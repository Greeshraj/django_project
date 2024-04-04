from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from .models import *
from .utils import calculate_attendance_stats 

def index(request):
    users = User.objects.all()
    user_details_with_attendance = []
    for user in users:
        user_info = {'name': user.get_full_name(), 'email': user.email}
        user_attendance = Attendance.objects.filter(user=user)
        user_details_with_attendance.append({'user_info': user_info, 'attendance': user_attendance})
    return render(request, 'index.html', {'user_details_with_attendance': user_details_with_attendance})

def registration(request):
    error=""
    if(request.method=="POST"):
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        empcode=request.POST['empcode']
        email = request.POST['email']
        pwd = request.POST['password']
        try:
            user = User.objects.create_user(first_name=fn,last_name=ln,username=email,email=email,password=pwd)
            EmployeeDetail.objects.create(user= user,empcode=empcode)
            Attendance.objects.create(user=user)
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





  # Import the function we defined

def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user_attendance = Attendance.objects.filter(user=request.user).exclude(date__isnull=True)
    user_attendance = user_attendance.exclude(date=None)
    user_details = EmployeeDetail.objects.filter(user=request.user)

    
    attendance_stats = []
    for user_detail in user_details:
        total_days, total_attendance,total_absent = calculate_attendance_stats(user_detail.joiningdate, user_attendance)
        attendance_stats.append({'total_days': total_days, 'total_attendance': total_attendance, 'total_absent':total_absent})

    return render(request, 'emp_home.html', {'user_attendance': user_attendance, 'user_details': user_details, 'attendance_stats': attendance_stats})

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


def attendance(request):
    error = None
    if not request.user.is_authenticated:
        error="yes"
        return redirect('emp_login')
    user = request.user

    if request.method == 'POST':
        # Check if attendance record already exists for today
        today = timezone.now().date()
        existing_attendance = Attendance.objects.filter(user=user, date=today).exists()
       
        if not existing_attendance:
            ctime=request.POST['ctime']
            # If attendance record doesn't exist, create a new one
            Attendance.objects.create(user=user, date=today, time_in=ctime)
            # Redirect to profile page or any other page as per your requirement
            error="no"
            return redirect('profile')
        else:
            # If attendance record already exists, set error message
            error = "already"
    return render(request, 'attendance.html', {'error': error})