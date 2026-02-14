# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from apps.authentication.models import User

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # print("Check1")
            user = authenticate(username=username, password=password)
            # print("Check2")
            if user is not None:
                # print("Check3")
                if user.is_superuser:
                    login(request, user)
                    return redirect("/index")
                if user.is_ent:
                    # print("Check4")
                    login(request, user)
                    # print("Redirecting to ent_index")
                    return redirect("/ent/profile")
                if user.is_investor:
                    login(request, user)
                    return redirect("/investor")
            
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get("user_type")    
            # form.save()
            if user_type == '1':
                user.is_ent = True
            else:
                user.is_investor = True
            user.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
