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
spacy.load('en_core_web_sm')

def convert_pdf_into_text(url):
    with fitz.open(url) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def resume_model():
    data = pd.read_csv('job_desc_csv_fixed_url.csv')
    x_train,x_test,y_train,y_test = train_test_split(data.job_descriptions,data.search_terms,random_state=0)
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
        return super(HomePageView,self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = "Hello CV"
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
