from django.urls import path,include
from .views import *

app_name = 'employee_resume'

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('login/',HRLoginPage.as_view(),name='login'),
    path('about-us/',AboutPageView.as_view(),name='about'),
    path('contact-us/',ContactPageView.as_view(),name='contact'),
    path('cv-prediction/',PredictionPageView.as_view(),name='cv'),
    path('employees/',EmployeePageView.as_view(),name='emp'),
    path('hr/',HRPageView.as_view(),name='hr'),
]