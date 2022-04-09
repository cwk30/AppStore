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
    rate = models.IntegerField()
    experience_req = models.IntegerField()
    job_requirement = models.TextField(('describe the job requirement'), max_length=500, blank=True)
    status = models.CharField(max_length=16,default='pending')

class nanny(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    rate = models.IntegerField()
    experience = models.IntegerField()
    about_me = models.TextField(('About me'), max_length=500,blank=True)
    
class appliednanny(models.Model):
    applyid = models.AutoField(primary_key = True)
    jobid = models.ForeignKey(jobs, on_delete=models.CASCADE)
    nannyid = models.ForeignKey(nanny, on_delete=models.CASCADE)
    status = models.CharField(max_length=16,default='pending')

class request(models.Model):
    requestid = models.AutoField(primary_key = True)
    fromparent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sample1')
    tositter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sample2')
    status = models.CharField(max_length=16, default='pending')