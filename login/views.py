from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('main')
        else:
            return render(request,'login/login.html',{'error_message':"에러"})
    else:
        return render(request,'login/login.html') # 여기 404 뜨게해야 할 것

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],password=request.POST["password1"])
            auth.login(request,user)
            return redirect('login')
        return render(request, 'login/signup.html')
    return render(request, 'login/signup.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

