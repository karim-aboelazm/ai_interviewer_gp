from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    resume = models.FileField(upload_to='resume/')

    def __str__(self):
        return f"Resume - [{self.id}]"

class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(Resume,on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    
    email = models.EmailField()
    
    score = models.IntegerField()

    prediction = models.CharField(max_length=200)

    def __str__(self):
        return f"Resume Analysis - [{self.id}] - done"

class HrModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    full_name = models.CharField(max_length=250)

    address = models.CharField(max_length=250,null=True,blank=True)

    image = models.ImageField(upload_to="hr_profile/")

    phone = models.CharField(max_length=15,null=True,blank=True)

    join_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name