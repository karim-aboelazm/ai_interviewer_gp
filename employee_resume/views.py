from django.shortcuts import render
from django.views.generic import TemplateView,CreateView,FormView,View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login , logout
from .models import *
from .forms import *
import pandas as pd
import numpy as np
import spacy
import fitz
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.linear_model import SGDClassifier
from django.urls import reverse_lazy,reverse
from .read_cv import get_resume_info
import random
from .courses import *
from django.http import HttpResponse

spacy.load('en_core_web_sm')

# def convert_pdf_into_text(url):
#     with fitz.open(url) as doc:
#         text = ""
#         for page in doc:
#             text += page.get_text()
#     return text

def resume_model():
    data = pd.read_csv('job_desc_csv_fixed_url.csv')
    x_train,x_test,y_train,y_test = train_test_split(data.job_descriptions,data.search_term,random_state=0)
    count_vect = CountVectorizer(stop_words='english')
    x_train_count = count_vect.fit_transform(x_train)
    trans = TfidfTransformer()
    x_train_tfidf = trans.fit_transform(x_train_count)
    clf = SGDClassifier(loss='hinge',penalty='l1',alpha=0.001,random_state=42,max_iter=5,tol=None)
    clf.fit(x_train_tfidf,y_train)
    preds = clf.predict(count_vect.transform(x_test))
    accuracy = np.mean(preds==np.array(y_test))
    return clf,count_vect,accuracy

def resume_predict(res_txt):
    text_to_series = pd.Series(res_txt)
    clf,count_vect,_ = resume_model()
    prediction = clf.predict(count_vect.transform(text_to_series))
    return prediction[0]

class ResumeMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and HrModel.objects.filter(user=request.user).exists()):
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)

class HomePageView(ResumeMixin,CreateView):
    template_name = 'home.html'
    form_class = ResumeForm
    success_url = '/'
    def form_valid(self, form):
        resume = form.cleaned_data.get('resume')
        self.request.session['is_posted'] = True
        return super(HomePageView,self).form_valid(form)
    
    def form_invalid(self, form):
        self.request.session['is_posted'] = False
        return super().form_invalid(form)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affine = AffineModel.objects.latest('id')
        if affine:
            token = affine.token
            ws = affine.workspace
        else:
            token , ws = None
        if token is not None and ws is not None:
            last_res_path = Resume.objects.latest('id')
            last_res_name = last_res_path.resume.name
            resume_name = last_res_name[last_res_name.index('/')+1:]
            path_res = f"media\\resume\\{resume_name}"
            res_text , resume_data = get_resume_info(path_res,token,ws)
            
            context['prediction'] = resume_predict(str(res_text))
            context['full_name'] = resume_data['full_name']
            context['email_address'] = resume_data['email_address'][0]
            context['phone_number'] = resume_data['phone_number']
            context['links'] = resume_data['links']
            context['date_of_birth'] = resume_data['date_of_birth']
            context['address'] = resume_data['address']
            edu = str(resume_data['education']).split(' - ')
            education = {'spcialize':edu[0],'org':edu[1],'dur':edu[2]}
            context['education'] = education
            context['total_experience'] = resume_data['total_experience']
            context['languages'] = resume_data['languages']
            context['profession'] = resume_data['profession']
            context['work_experience'] = resume_data['work_experience']
            context['skills'] = resume_data['skills']
            context['is_posted'] = self.request.session.get('is_posted')
            context["resume_score"] = 0
            text = str(res_text)
            if 'Objective' in text or 'objective' in text:
                context['objective'] = "Awesome! You have added Objective"
                context["resume_score"] += 20
            else:
                context['objective'] = "According to our recommendation please add your career objective, it will give your career intension to the Recruiters."
            
            if 'Declaration' in text or 'declaration' in text:
                context['declaration'] = "Awesome! You have added Declaration"
                context["resume_score"] += 20
            else: 
                context['declaration'] = "According to our recommendation please add Declaration✍. \nIt will give the assurance that everything written on resume is true and fully acknowledged by you"
            
            if 'Hobbies' or 'Interests' in text or ('hobbies' or 'interests'in text):
                context['hobbies'] = "Awesome! You have added Hobbies"
                context["resume_score"] += 20
            else:
                context['hobbies'] = "According to our recommendation please add Hobbies⚽.\nIt will show your persnality to the Recruiters and give the assurance that you are fit for this role or not."
            
            if 'Achievements' in text or 'achievements' in text:
                context['achievements'] = "Awesome! You have added Achievements"
                context["resume_score"] += 20
            else:
                context['achievements'] = "According to our recommendation please add Achievements🏅. \nIt will show that you are capable for the required position."
            
            if 'Projects' in text or 'projects' in text:
                context['projects'] = "Awesome! You have added Projects"
                context["resume_score"] += 20
            else:
                context['projects'] = "According to our recommendation please add Projects📝. \nIt will show your skills and knowledge about the required position."
            
            if 'Python' in context['prediction']:
                context['courses_list']= [link for link in random.sample(Python_Courses, 6)]
            if 'ui' in context['prediction']:
                context['courses_list']= [link for link in random.sample(Ui_Courses, 6)]
            if 'web' in context['prediction']:
                context['courses_list']= [link for link in random.sample(Web_Courses, 6)]
            if 'JavaScript' in context['prediction']:
                context['courses_list']= [link for link in Js_Courses]
            elif 'android' in context['prediction']:
                context['courses_list']= [link for link in random.sample(Android_Courses, 6)]

            context['resume_improve']= [link for link in random.sample(resume_videos, 4)]

            context['interview_improve']= [link for link in random.sample(interview_videos, 4)]
            
            if not ResumeAnalysis.objects.filter(email=context['email_address']).exists():
                ResumeAnalysis.objects.create(
                    resume = last_res_path,
                    name = context['full_name'],
                    email = context['email_address'],
                    score = context['resume_score'],
                    phone = context['phone_number'],
                    prediction = context['prediction']
                )
        return context
    
class AboutPageView(TemplateView):
    template_name = 'about.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html'

class PredictionPageView(TemplateView):
    template_name = 'cv.html'
    
class EmployeePageView(TemplateView):
    template_name = 'emp.html'

class HRPageView(TemplateView):
    template_name = 'hr.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resume_analysis"] = ResumeAnalysis.objects.all()
        return context
    
class HRLoginPage(FormView):
    template_name = 'login.html'
    form_class = HRLoginForm
    success_url = reverse_lazy('employee_resume:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        userpassword = form.cleaned_data.get('userpassword')
        usr = authenticate(username=username,password=userpassword)
        if usr is not None and HrModel.objects.filter(user=usr).exists():
            login(self.request,usr)
        else:
            return render(self.request,self.template_name,{'form':self.form_class})
        return super().form_valid(form)
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url

class HRLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('employee_resume:login')

class InterViewPage(FormView):
    template_name = 'interview.html'
    form_class = QuestionsReviewsForm
    success_url = reverse_lazy('employee_resume:interview')
    def form_valid(self, form):
        current_user = self.request.user
        q_id = form.cleaned_data.get('question_id')
        u_a = form.cleaned_data.get('user_answer')
        if q_id and u_a:
            question = InterViewQuestion.objects.filter(pk=q_id).first()
            rec = InterviewQuestionReview.objects.create(user=current_user,question=question,user_answer=str(u_a).strip().upper())
            rec.save(force_insert=False)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_questions = InterViewQuestion.objects.all()
        context["all_questions"] = all_questions
        return context
    
    