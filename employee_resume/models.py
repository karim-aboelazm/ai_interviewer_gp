from typing import Iterable
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

    phone = models.CharField(max_length=30)
    
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
    
class AffineModel(models.Model):
    token = models.CharField(max_length=250,verbose_name='Affine Token')
    workspace = models.CharField(max_length=50,verbose_name='Affine Workspace')
    def __str__(self):
        return f"Affine Data [{self.id}]"

class Job(models.Model):
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    job_responsibilities = models.TextField()
    job_requirements = models.TextField()
    job_preferred_qualifications = models.TextField()
    job_preferred_qualifications = models.TextField()
    job_salary = models.IntegerField()
    def __str__(self):
        return self.job_title
    
ANSWERS = [(i.upper(),i.upper()) for i in ['a','b','c','d']]

class InterViewQuestion(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    question_text =  models.CharField(max_length=250)
    question_text_des =  models.TextField(null=True,blank=True)
    question_image =  models.FileField(upload_to='interviewer/images',null=True,blank=True)
    question_image_des =  models.TextField(null=True,blank=True)
    answer_one = models.CharField(verbose_name=('Answer A'),max_length=200)
    answer_two = models.CharField(verbose_name=('Answer B'),max_length=200)
    answer_three = models.CharField(verbose_name=('Answer C'),max_length=200)
    answer_four = models.CharField(verbose_name=('Answer D'),max_length=200)
    correct_answer = models.CharField(choices=ANSWERS,max_length=5)
    def __str__(self):
        return f"Question - ({self.id}) for job ({self.job.job_title})"


class InterviewQuestionReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(InterViewQuestion,on_delete=models.CASCADE)
    correct_answer = models.CharField(max_length=5,null=True,blank=True)
    user_answer = models.CharField(choices=ANSWERS,max_length=5,null=True,blank=True)
    answer_rate = models.IntegerField(default=0)
    def save(self,** kwargs):
        if self.question:
            self.correct_answer = self.question.correct_answer
        if self.user_answer:
            if self.user_answer == self.correct_answer:
                self.answer_rate = 1
            else:
                self.answer_rate = 0                
        return super().save()
    
    def __str__(self):
        obj = f"{self.user} has choosed ({self.user_answer})"
        if self.correct_answer == self.user_answer:
            obj = f"{self.user.username} has passed from this question"
        else:
            obj = f"{self.user.username} has failed from this question"
        return obj
