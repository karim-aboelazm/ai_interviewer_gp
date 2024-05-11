from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'employee_resume'

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('login/',HRLoginPage.as_view(),name='login'),
    path('about-us/',AboutPageView.as_view(),name='about'),
    path('contact-us/',ContactPageView.as_view(),name='contact'),
    path('cv-prediction/',PredictionPageView.as_view(),name='cv'),
    path('employees/',EmployeePageView.as_view(),name='emp'),
    path('hr/',HRPageView.as_view(),name='hr'),
    path('interview/',InterViewPage.as_view(),name='interview'),
    path('logout/',HRLogoutView.as_view(),name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
