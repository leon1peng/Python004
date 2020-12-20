from django.shortcuts import render, redirect
from django import forms
from django.forms import widgets
from django.contrib import auth
from django.contrib.auth.models import User


# Create your views here.
class LoginForm(forms.Form):
    user = forms.CharField(label="用户名", min_length=3, max_length=8,
                           error_messages={"min_length": "用户名太短", "required": "必填"})
    pwd = forms.CharField(label="密 码", min_length=5,
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                          error_messages={"min_length": "密码太短", "required": "必填"}
                          )


def login_f(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            print(login_form.cleaned_data)
        else:
            print(login_form.cleaned_data)
            return render(request, 'login.html', locals())
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# --------------------auth认证
def login(request):
    if request.method == "POST":
        print(request.POST)
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user, pwd)
        user = auth.authenticate(username=user, password=pwd)
        user_obj = User.objects.filter(username=user).first()
        print(user_obj)
        if user_obj:
            print(user_obj.username, user_obj.password)
        if user:
            auth.login(request, user)
            print('user2:', request.user)
            return render(request, 'home.py')
    return redirect('/form/')


def home(request):
    print("home page")
    user = request.user
    if not user.is_authenticated():
        return redirect("/login/")
    username = user.username
    print(username)
    return render(request, 'index.html', locals())


def logout(request):
    print('logout')
    auth.logout(request)
    return redirect('/login/')


def reg(request):
    print("reg")
    if request.method == "GET":
        print("get reg")
        return render(request, 'reg.html')
    elif request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        print(user, pwd)
        user = User.objects.create_user(username=user, password=pwd)
        return redirect('/login/')
    return render(request, 'reg.html', locals())
