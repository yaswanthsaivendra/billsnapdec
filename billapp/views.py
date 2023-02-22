from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import Profile
from plans.models import Plan

def index(request):
    return render(request, 'index.html')

def sett_ings(request):
    return render(request, 'settings.html')

def dashboard(request):
    return render(request, 'dashboard.html')


def dashcustomer(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    return render(request,'customerdash.html', {'profile':user_profile})

def customer_plans(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    plans = user_profile.plans.all()
    print(plans)
    return render(request,'customerplans.html', {'plans':plans})

def sending(request):
    l=[]
    for i in range(10):
        l.append(i)
        return render(request,'sending.html',{'slug':l})