from django.contrib import admin
from .models import *

# OopCompanion:suppressRename

all_models = [
    Resume,
    ResumeAnalysis,
    HrModel,
    AffineModel,
    Job,
    InterViewQuestion,
    InterviewQuestionReview,
    ApplicantModel]
[admin.site.register(model) for model in all_models]

# class IndecatorModelAdmin(admin.ModelAdmin):
#     list_display = ['username', 'first_name', 'last_name', 'email', 'is_hr_employee', 'is_indecator']
#     fields = ['username', 'password', 'first_name', 'last_name', 'email', 'profile', 'resume', 'is_hr_employee',
#               'is_indecator']


# admin.site.register(IndecatorModel)
