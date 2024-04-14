from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    resume = models.FileField(
        name="Resume Name",
        upload_to='resume/'
    )
    def __str__(self):
        return f"Resume - [{self.id}]"

class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(
        Resume,
        name="Resume",
        on_delete=models.CASCADE
    )
    name = models.CharField(
        name="Candidate Name",
        max_length=200
    )
    email = models.EmailField(
         name="Candidate Email",
    )
    score = models.IntegerField(
         name="Candidate Score",
    )
    prediction = models.CharField(
        name="Candidate Resume Prediction",
        max_length=200
    )
    def __str__(self):
        return f"Resume Analysis - [{self.id}] - done"

class HrModel(models.Model):
    user = models.OneToOneField(
        User,
        name="Hr Username",
        on_delete=models.CASCADE
    )
    full_name = models.CharField(
        name="Hr Full Name",
        max_length=250
    )
    address = models.CharField(
        name="Hr Address",
        max_length=250,
        null=True,
        blank=True
    )
    image = models.ImageField(
        name="Hr Profile Image",
        upload_to="hr_profile/"
    )
    phone = models.CharField(
        name="Hr Phone Number",
        max_length=15,
        null=True,
        blank=True
    )
    join_on = models.DateTimeField(
        name="Hr Join On",
        auto_now_add=True
    )
    def __str__(self):
        return self.full_name