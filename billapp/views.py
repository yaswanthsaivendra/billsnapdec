from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def sett_ings(request):
    return render(request, 'settings.html')

def dashboard(request):
    return render(request, 'dashboard.html')


def dashcustomer(request):
    return render(request,'customerdash.html')

def sending(request):
    l=[]
    for i in range(10):
        l.append(i)
        return render(request,'sending.html',{'slug':l})