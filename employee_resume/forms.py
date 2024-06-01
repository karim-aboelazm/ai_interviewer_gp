from django import forms
from .models import *


# OopCompanion:suppressRename

# upload resume form
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'

class HRLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    userpassword = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            pass
        else:
            raise forms.ValidationError('hr with this username does not exists')
        return user_name

class QuestionsReviewsForm(forms.Form):
    ANSWERS = [(i.upper(), i.upper()) for i in ['a', 'b', 'c', 'd']]
    user_answer = forms.ChoiceField(choices=ANSWERS, widget=forms.Select())
    question_id = forms.IntegerField(widget=forms.NumberInput())




class ApplicantRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = ApplicantModel
        fields = [
            'username',
            'full_name',
            'password',
            'phone',
            'address',
            'email'
        ]
        
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError('Patient with this username is already exists ! please try again :( ')
        return user_name

class ApplicantLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            return user_name
        else:
            raise forms.ValidationError('Applicant with this username does not exist. Please try again.')

class ApplicantUpdateForm(forms.ModelForm):
    class Meta:
       model = ApplicantModel
       fields = [
           'full_name',
           'address',
           'phone',
           'image',
           ]

class ApplicantForgetPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Your Email Here ...'
    }))
    def clean_email(self):
        e = self.cleaned_data.get('email')
        if ApplicantModel.objects.filter(user__email = e).exists():
            pass
        else:
            raise forms.ValidationError('Applicant With This Email Does Not Exists.')
        return e
    
class ApplicantResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Enter Your New password'
    }),label='New Password')
    
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Confirm Your New password'
    }),label='Confirm New Password')
    
    def clean_confirmation_new_password(self):
        new_pass = self.cleaned_data.get('new_password')
        c_new_pass =  self.cleaned_data.get('confirm_new_password')
        if new_pass != c_new_pass:
            raise forms.ValidationError('Passwords are not match !')
        return c_new_pass




class HrRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = HrModel
        fields = [
            'username',
            'full_name',
            'email',
            'password',
            'phone',
            'address',
        ]
        
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError('Patient with this username is already exists ! please try again :( ')
        return user_name

class HrLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            return user_name
        else:
            raise forms.ValidationError('Hr with this username does not exist. Please try again.')

class HrUpdateForm(forms.ModelForm):
    class Meta:
       model = HrModel
       fields = [
           'full_name',
           'address',
           'phone',
           'image',
           ]

class HrForgetPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Your Email Here ...'
    }))
    def clean_email(self):
        e = self.cleaned_data.get('email')
        if HrModel.objects.filter(user__email = e).exists():
            pass
        else:
            raise forms.ValidationError('Hr With This Email Does Not Exists.')
        return e
    
class HrResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Enter Your New password'
    }),label='New Password')
    
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Confirm Your New password'
    }),label='Confirm New Password')
    
    def clean_confirmation_new_password(self):
        new_pass = self.cleaned_data.get('new_password')
        c_new_pass =  self.cleaned_data.get('confirm_new_password')
        if new_pass != c_new_pass:
            raise forms.ValidationError('Passwords are not match !')
        return c_new_pass
