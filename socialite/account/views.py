
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'account/signup.html')

def signup(request):
    if request.method=='POST':
        mail=request.POST.get('email','')
        username=request.POST.get('username','')
        name=request.POST.get('name','')
        password=request.POST.get('password','')
        conf_password=request.POST.get('confirm_password','')

        userCheck=User.objects.filter(username=username)
        if userCheck:
            messages.error(request,'sorry! user name allready define ')
            return redirect('/')
    
        print(f"{mail=}")
        print(f"{username=}")
        print(f"{name=}")
        print(f"{password=}")
        print(f"{conf_password=}")

        if password==conf_password:
            user_obj=User.objects.create_user(first_name=name,password=password,email=mail,username=username)
            user_obj.save()


        return redirect('/')

def user_login(request):
    if request.method=='POST':
        user_name=request.POST.get('username','')
        user_password=request.POST.get('password','')

        user=authenticate(username=user_name,password=user_password)

        if user is not None:
            login(request,user)
            messages.success(request,'you logged in')
            return redirect('/userpage')

        else:
            messages.error(request,'invallid crediantial')
            return redirect('/')    

def user_logout(request):
    logout(request)
    messages.success(request,'logged out')
    return redirect('/')
