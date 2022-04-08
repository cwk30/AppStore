from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class usersext(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nric= models.CharField(max_length=9, unique=True)
    dob = models.DateField()
    role = models.CharField(max_length=16)

class jobs(models.Model):
    jobid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    rate = models.CharField(max_length = 5)
    experience_req = models.CharField(max_length = 3)
    job_requirement = models.TextField(('describe the job requirement'), max_length=500, blank=True)

class nanny(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    rate = models.CharField(max_length = 5)
    experience = models.CharField(max_length = 3)
    about_me = models.TextField(('describe yourself'), max_length=500,blank=True)

class appliednanny(models.Model):
    applyid = models.AutoField(primary_key = True)
    jobid = models.ForeignKey(jobs, on_delete=models.CASCADE)
    nannyid = models.ForeignKey(nanny, on_delete=models.CASCADE)
