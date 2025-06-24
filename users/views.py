from django.shortcuts import render,redirect
from django.contrib.auth.models import User#since the auth module is not created by us, we have to import it for user creation.
#Authentication........
from django.contrib.auth import login as authlogin,logout as authlogout
from django.contrib.auth import authenticate

# Create your views here.
def login(request):
    user=None
    error_message=None
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password) #this fun will verifies username & password from db, if exists the user object will be returned
        if user:
            authlogin(request,user)
            return redirect('list')
        else:
            error_message='invalid credentials'
    return render(request,'users/login.html',{'error_message':error_message})

def logout(request):
    authlogout(request)
    return redirect('login')
def signup(request):
    user=None
    error_message=None
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=User.objects.create_user(username=username,password=password)
        except Exception as e:
            error_message=str(e)
    return render(request,'users/create.html',{'user':user,'error_message':error_message})

 