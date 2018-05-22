# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Users(models.Model):
  Name = models.CharField(max_length=255)
  Username =  models.CharField(max_length=255) 
  Password =      models.CharField(max_length=255)
  Created_at = models.DateTimeField(auto_now = True) 
  Updated_at = models.DateTimeField(auto_now = True)

class Trips(models.Model):
  Tripuser = models.ForeignKey(Users, related_name="Trips")
  Destination = models.CharField(max_length=255)
  Description = models.TextField()
  Startdate   =  models.DateField()
  Enddate     =  models.DateField()
  Guests     =   models.ManyToManyField(Users, related_name="Trips_people",null=True)
  Created_at = models.DateTimeField(auto_now = True) 
  Updated_at = models.DateTimeField(auto_now = True)
