import profile
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Profile
from .models import customer,csvs
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from logging.handlers import TimedRotatingFileHandler
import logging
from plans.models import *

logger=logging.getLogger()
logging.basicConfig(
        handlers=[ TimedRotatingFileHandler('logs.log', when="midnight", interval=1)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

from django.contrib.auth.models import User
from apps.models import applists

# Create your views here.
'''def addcustomer(request,slug):
    app=applists.objects.get(slug=slug)
    addcus=customer()
    if request.method=='POST':
        app=app
        utility_name = request.POST.get('utility_name')
        utility_short_name= request.POST.get('utility_short_name')
        utility_state= request.POST.get('utility_state')
        utility_district= request.POST.get('utility_district')
        utility_country=request.POST.get('utility_country')
        utility_postalcode= request.POST.get('utility_postalcode')
        utility_address=request.POST.get('utility_address')

        #contact details
        contact_person= request.POST.get('contact_person')
        contact_email = request.POST.get('contact_email')
        contact_phnum =request.POST.get('contact_phnum')
        contact_mobile=request.POST.get('contact_mobile')
        contact_designation= request.POST.get('contact_designation')
        contact_landline=request.POST.get('contact_landline')

        emergency_person=request.POST.get('emerg_person')
        emergency_altperson=request.POST.get('emerg_altperson')
        emergency_mobile=request.POST.get('emerg_mobile')
        emergency_altmobile=request.POST.get('emerg_altmobile')
        emergency_officeaddress=request.POST.get('emerg_officeaddress')
        emergency_altofficeaddress=request.POST.get('emerg_altofficeaddress')

        #contact details
        addcus.utility_name =utility_name
        addcus.utility_short_name = utility_short_name
        addcus.utility_state = utility_state
        addcus.utility_district = utility_district
        addcus.utility_country = utility_country
        addcus.utility_postalcode = utility_postalcode
        addcus.utility_address=utility_address

        addcus.contact_person = contact_person
        addcus.contact_email=contact_email
        addcus.contact_phnum=contact_phnum
        addcus.contact_mobile=contact_mobile
        addcus.contact_designation=contact_designation
        addcus.contact_landline=contact_landline

        addcus.emergency_person=emergency_person
        addcus.emergency_altperson=emergency_altperson
        addcus.emergency_mobile=emergency_mobile
        addcus.emergency_altmobile=emergency_altmobile
        addcus.emergency_officeaddress=emergency_officeaddress
        addcus.emergency_altofficeaddress=emergency_altofficeaddress

        addcus.save()
        return redirect('customerlist')
    else:
        return render(request, 'addcustomer.html',{'slug':slug})'''
from .forms import CustomerCreateForm

@login_required
def addcustomer(request):
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST)
        if request.user == app.author:
            if form.is_valid():
                customer.objects.create(
                    utility_name = request.POST.get('utility_name'),
        utility_short_name= request.POST.get('utility_short_name'),
        utility_state= request.POST.get('utility_state'),
        utility_district= request.POST.get('utility_district'),
        utility_country=request.POST.get('utility_country'),
        utility_postalcode= request.POST.get('utility_postalcode'),
        utility_address=request.POST.get('utility_address'),
        contact_person= request.POST.get('contact_person'),
        contact_email = request.POST.get('contact_email'),
        contact_phnum =request.POST.get('contact_phnum'),
        contact_mobile=request.POST.get('contact_mobile'),
        contact_designation= request.POST.get('contact_designation'),
        contact_landline=request.POST.get('contact_landline'),
        emergency_person=request.POST.get('emerg_person'),
        emergency_altperson=request.POST.get('emerg_altperson'),
        emergency_mobile=request.POST.get('emerg_mobile'),
        emergency_altmobile=request.POST.get('emerg_altmobile'),
        emergency_officeaddress=request.POST.get('emerg_officeaddress'),
        emergency_altofficeaddress=request.POST.get('emerg_altofficeaddress'),
                )
                return redirect('customerlist', slug=slug)
        else :
            return redirect('home')
    else :
        form = CustomerCreateForm()
    return render(request, 'addcustomer.html', {'form' :form})

@login_required
def customerlist(request,slug):
    app=applists.objects.get(slug=slug)
    details = Profile.objects.filter(apps=app).values_list('user__username', 'slug', 'id')
    return render(request, 'customerlist.html', {'details':details, 'slug':slug})
    
@login_required
def deletecust(request,utility_name):
    deli=customer.objects.get(utility_name=utility_name)
    deli.delete()
    logger.info(request.user.username+"_deleted the"+deli.utility_name)
    return redirect('customerlist')

@login_required
def updaterecord(request,id):
    inst=customer.objects.get(id=id)
    if request.method=='POST':
        utility_name = request.POST.get('utility_name')
        utility_short_name= request.POST.get('utility_short_name')
        utility_state= request.POST.get('utility_state')
        utility_district= request.POST.get('utility_district')
        utility_country=request.POST.get('utility_country')
        utility_postalcode= request.POST.get('utility_postalcode')
        #contact details
        contact_person= request.POST.get('contact_person')
        contact_email = request.POST.get('contact_email')
        contact_phnum =request.POST.get('contact_phnum')
        contact_designation= request.POST.get('contact_designation')
        office_address=request.POST.get('office_address')
        instance=customer.objects.get(id=id)
        #contact details
        instance.utility_name =utility_name
        instance.utility_short_name = utility_short_name
        instance.utility_state = utility_state
        instance.utility_district = utility_district
        instance.utility_country = utility_country
        instance.utility_postalcode = utility_postalcode
        instance.contact_person = contact_person
        instance.contact_email=contact_email
        instance.contact_phnum=contact_phnum
        instance.contact_designation=contact_designation
        instance.office_address=office_address
        instance.save()

        return redirect('customerlist')
    else:
        return render(request, 'editcustomer.html',{'profile': inst})

import pandas as pd
@login_required
def bulk_upload(request,slug):
    if request.method=='POST':
        csvfile=request.FILES.get('csvfile')
        df=pd.read_csv(csvfile)
        l=list(df.columns)
        if l==['LatD', ' "LatM"', ' "LatS"', ' "NS"', ' "LonD"', ' "LonM"', ' "LonS"', ' "EW"', ' "City"', ' "State"']:
            objs = [csvs(
                LatD= row['LatD'],
                LatM  = row[' "LatM"'],
                LatS= row[' "LatS"'],
                NS= row[' "NS"'],
                LonD  = row[' "LonD"'],
                LonM  = row[' "LonM"'],
                LonS  = row[' "LonS"'],
                EW  = row[' "EW"'],
                City  = row[' "City"'],
                State= row[' "State"']
                )
            for i,row in df.iterrows()]
            csvs.objects.bulk_create(objs)
            return redirect('uploadlist')
        else:
            status=0
            return render(request, 'bulkupload.html',{'stat':status})
    else:
        stat=00
        return render(request, 'bulkupload.html',{'stat':stat})
@login_required
def uploadlis(request):
    cols=[f.name for f in csvs._meta.get_fields()]
    dets=csvs.objects.all()
    return render(request,'uploadlist.html',{'details':dets,'columns':cols})

@login_required
def dashboard(request, slug):
    return render(request, 'dashboard.html', {'slug' : slug})

def add_customer_form(request, slug):
    app = applists.objects.get(slug=slug)
    return render(request, 'add_customer_app.html', {'app': app})

def add_existing_user(request, slug):
    profiles = Profile.objects.filter(admin=False).exclude(apps__slug=slug)
    app = applists.objects.get(slug=slug)
    return render(request, 'add_existing_user.html', {'profiles': profiles, 'app': app})

def add_customer_app(request, slug):
    username = request.GET.get('username')
    profile = Profile.objects.get(user__username=username)
    app = applists.objects.get(slug=slug)
    profile.apps.add(app)
    return redirect('customerlist',slug=slug)

def addingcustomer(request,slug):
    prof=Profile.objects.get(user=request.user)
    app=applists.objects.get(slug=slug)
    prof.apps.add(app)
    return redirect('customerlist',slug=slug)

def update_profile_plan(request, slug):
    profile = Profile.objects.get(slug__iexact=slug)

    new_plan = Plan.objects.get(id=request.POST.get('update_to'))
    new_paid_status = True if request.POST.get('paid')=='on' else False
    new_active_status = True if request.POST.get('plan_active')=='on' else False

    pre_plan = profile.plans.filter(app__appname=new_plan.app.appname)
    if pre_plan:
        pre_plan=pre_plan.first()
        profile.plans.remove(pre_plan)
        
    profile.plans.add(new_plan)
    profile.plan_active = new_active_status
    profile.paid = new_paid_status
    print(new_active_status, new_plan, new_paid_status)
    profile.save(update_fields=['plan', 'plan_active', 'paid'])
    return redirect('show_profile', profile.slug, new_plan.app.slug)