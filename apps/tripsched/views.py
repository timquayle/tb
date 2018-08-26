# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

import re, bcrypt,datetime
from datetime import datetime
from models import *
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
#main login/registration page
def index(request):
 if 'username' in request.session:
  #skip registration and login if we have already been here
  userinfo = Users.objects.get(Username=request.session['username'])

  usertrips = Trips.objects.raw("SELECT DISTINCT TRIPSCHED_TRIPS.id, TRIPSCHED_TRIPS.STARTDATE, TRIPSCHED_TRIPS.ENDDATE FROM TRIPSCHED_TRIPS\
  LEFT JOIN TRIPSCHED_TRIPS_GUESTS ON TRIPSCHED_TRIPS.ID = TRIPSCHED_TRIPS_GUESTS.TRIPS_ID\
  WHERE TRIPUSER_ID={0} OR TRIPSCHED_TRIPS_GUESTS.USERS_ID={0}".format(userinfo.id))
  
  otrips=Trips.objects.exclude(Tripuser=userinfo.id)
  othertrips=otrips.exclude(Guests=userinfo.id)
 
  context = {
  "username": request.session["username"],
   "trips": usertrips,
   "othertrips": othertrips
    }
 


  return render(request,'tripsched/homepage.html',context) 
 else:
  #else index.html contains registration form
  return render(request,'tripsched/index.html') 
#processing and validation of registration info
def process_registration(request):
  #due the validation on all of the inputs
  errors = []
  errors = validate(request.POST)
  if len(errors):
   context = {
   "errorlist": errors,
             }
   return render(request,'tripsched/index.html',context)
  #if it passed validation, write it to the database
  else:
   if request.method == 'POST':
    name = request.POST['name']
    user =   request.POST['username']
    password =   request.POST['password']
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    Users.objects.create(Name=name,Username=user,Password=hash_password)   
    request.session["username"] = user
    userinfo = Users.objects.get(Username=request.session['username'])
    return redirect('/')

#checking login/password vs our database info
def loginchk(request):
 #route for people who have an account, but no session info stored
  if request.method == "POST":
   errors = []
   user =   request.POST['username']
   password =   request.POST['password']
  
   if len(user) < 3:
       errors.append("Username must be at least 3 characters")
   if len(password) < 8:
       errors.append("Password must be at least 8 characters!")
   if len(errors):
      context = {
     "lerrorlist": errors,
             }
      return render(request,'tripsched/index.html',context)
   
 #is the email contained in the database?
   try:
    userdb = Users.objects.get(Username=user)
  #if not flag a login/password error 
   except:
    context = {
      "loginerror": "Invalid Login or Password"         }

    return render(request,'tripsched/index.html',context)
   dbpassword=userdb.Password
   
   if(bcrypt.checkpw(password.encode(),dbpassword.encode())):
    
    request.session['username'] = user
    return redirect('/') 
   else:
    context = {
      "loginerror": "Invalid Login or Password"         }

    return render(request,'tripsched/index.html',context)

def newtrippage(request):
 
  return render(request,'tripsched/addtrip.html') 


def processtrip(request):
   if request.method=="POST":
    #due the validation on all of the inputs
    nodt = datetime.now()
    errors = []
    destination = request.POST['destination']
    description = request.POST['description']
    datefrom = request.POST['datefrom']
    dateto =   request.POST['dateto']
    if datefrom != "":
     dfstring = str(datefrom)
     datefromdt= datetime.strptime(dfstring, '%Y-%m-%d')
    if dateto != "":
     dtstring = str(dateto)
     datetodt= datetime.strptime(dtstring, '%Y-%m-%d')
    if len(destination) < 1:
       errors.append("Destination must not be blank!")
    if len(description) < 1:
       errors.append("Description must not be blank!")
    if len(datefrom) < 1:
       errors.append("Travel Date From date must not be blank!")  
    elif datefromdt <= nodt:
       errors.append("Travel Date from Date must be set in future!")
    if len(dateto) < 1:
       errors.append("Travel Date to date must not be blank!")
    elif datetodt <= nodt:
       errors.append("Travel Date from Date must be set in future!")
    elif datefromdt > datetodt:
       errors.append("Travel Date FromDate must be Less than Travel Date ToDate!")

    if len(errors):
      context = {
     "errorlist": errors,
             }
      return render(request,'tripsched/addtrip.html',context)
    else:
     userinfo = Users.objects.get(Username=request.session['username'])
     Trips.objects.create(Tripuser_id=userinfo.id,Destination=destination,Description=description,Startdate=datefrom,Enddate=dateto)
     return redirect('/')
     
def destinationpage(request,number):
  trip=Trips.objects.get(id=number)
  #plan= Trips.objects.raw("SELECT TRIPSCHED_TRIPS.id, TRIPSCHED_USERS.NAME FROM TRIPSCHED_TRIPS JOIN TRIPSCHED_USERS ON TRIPUSER_ID = TRIPSCHED_USERS.id \
  #  WHERE TRIPSCHED_TRIPS.id = {0}".format(trip.id))
  guests=dir('Trips.Guests')
  print guests
  #guests= Trips.objects.raw("SELECT TRIPSCHED_TRIPS_GUESTS.id, TRIPSCHED_USERS.NAME FROM TRIPSCHED_TRIPS_GUESTS\
  #  JOIN TRIPSCHED_USERS ON USERS_ID = TRIPSCHED_USERS.id \
  #  WHERE TRIPSCHED_TRIPS_GUESTS.trips_id = {0}".format(trip.id))
  #guests = trip.Guests.all()
  #guests= Trips.objects.filter(id=trip.id)
  context = {
  "trip": trip,
  "guests": guests,
  #"plan": plan
  
  }
  
  return render(request,'tripsched/destination.html',context)     
#validation function
def processjoin(request,number):
  userinfo = Users.objects.get(Username=request.session['username'])
  this_trip = Trips.objects.get(id=number)
  this_user = userinfo.id
  this_trip.Guests.add(this_user)
  return redirect('/')
def validate(rp):
  #remember to add validation to login, i have to ask why validate login information? the more the precise the 
  #information returned, the more the hackers like it.
   errors = []
   name = rp['name']
   username = rp['username']
   password = rp['password']
   cpassword = rp['cpassword']

   if len(name) < 3:
       errors.append("Name must be at least 3 characters!")
   elif not NAME_REGEX.match(name):
       errors.append("Name must only contain letters!")
   if len(username) < 3:
       errors.append("Username must be at least 3 characters")
   if len(password) < 8:
       errors.append("Password must be at least 8 characters!")    
   elif len(cpassword) < 1:
       errors.append("Please Enter Confirmation Password!")    
   elif(password != cpassword):
       errors.append("Password and confirm password must match!")
   return errors
#logout of session
def logout(request):
 del request.session["username"]
 return redirect('/')

