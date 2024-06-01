from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'employee_resume'

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    # path('login/',HRLoginPage.as_view(),name='login'),
    # path('about-us/',AboutPageView.as_view(),name='about'),
    path('contact-us/',ContactPageView.as_view(),name='contact'),
    path('cv-prediction/',PredictionPageView.as_view(),name='cv'),
    path('employees/',EmployeePageView.as_view(),name='emp'),
    path('hr/',HRPageView.as_view(),name='hr'),
    path('interview/<str:job_title>',InterViewPage.as_view(),name='interview'),
    path('interview_results/',InterViewResults.as_view(),name='interview_results'),
    # path('logout/',HRLogoutView.as_view(),name='logout'),
    path('applicant-signup/',ApplicantRegisterView.as_view(),name='applicant_signup'),  
    path('applicant-login/',ApplicantLoginView.as_view(),name='applicant_login'), 
    path('applicant-profile/',ApplicantProfileView.as_view(),name='applicant_profile'), 
    path('applicant-edit-profile/<int:pk>',ApplicantUpdateView.as_view(),name='applicant_edit_profile'), 
    path('applicant-forget-password/',ApplicantForgetPasswordView.as_view(),name='applicant_forget_password'), 
    path('applicant-reset-password/<email>/<token>/',ApplicantResetPasswordView.as_view(),name='applicant_reset_password'), 
 
    path('hr-login/',HRLoginView.as_view(),name='hr_login'), 
    path('hr-profile/',HRProfileView.as_view(),name='hr_profile'), 
    path('hr-edit-profile/<int:pk>',HRUpdateView.as_view(),name='hr_edit_profile'), 
    path('hr-forget-password/',HRForgetPasswordView.as_view(),name='hr_forget_password'), 
    path('hr-reset-password/<email>/<token>/',HRResetPasswordView.as_view(),name='hr_reset_password'), 

    
    
    path('logout/',ApplicantLogoutView.as_view(),name='logout'), 
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
