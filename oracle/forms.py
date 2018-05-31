from django import forms
from django.forms import extras
from .models import JobApplication, Feedback, ApplicantList, Position

class ApplicantListForm(forms.ModelForm):
    class Meta :
        model = ApplicantList
        fields = '__all__'

class PositionForm(forms.ModelForm):
    prefix = 'add_position'
    class Meta:
        model = Position
        fields = '__all__'

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = '__all__'
        widgets = {'applied_date': forms.DateInput(attrs={'type': 'date'}),
                    'spm_graduated_year': forms.SelectDateWidget(years=range(1960, 2050)),
                    'highest_graduated_year': forms.SelectDateWidget(years=range(1960, 2050)),
                    'professional_graduated_year': forms.SelectDateWidget(years=range(1960, 2050)),
                    'date_employed_1': forms.DateInput(attrs={'type': 'date'}),
                    'date_end_1': forms.DateInput(attrs={'type': 'date'}),
                    'date_employed_2': forms.DateInput(attrs={'type': 'date'}),
                    'date_end_2': forms.DateInput(attrs={'type': 'date'}),
                    'date_employed_3': forms.DateInput(attrs={'type': 'date'}),
                    'date_end_3': forms.DateInput(attrs={'type': 'date'}),
                    'available_joining_date': forms.SelectDateWidget(years=range(2018, 2050)),
                    'disclaimer_date': forms.DateInput(attrs={'type': 'date'})}

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        widgets = {'interview_date': forms.DateInput(attrs={'type': 'date'}),
                    'feedback_time': forms.DateInput(attrs={'type': 'date'}),
                    'grooming': forms.RadioSelect(),
                    'body_language': forms.RadioSelect(),
                    'eye_contact': forms.RadioSelect(),
                    'confidence': forms.RadioSelect(),
                    'teamwork': forms.RadioSelect(),
                    'responsible': forms.RadioSelect(),
                    'professional': forms.RadioSelect(),
                    'communication': forms.RadioSelect(),
                    'ability_to_learn': forms.RadioSelect(),
                    'punctuality': forms.RadioSelect(),
                    'qualification': forms.RadioSelect(),
                    'skills': forms.RadioSelect(),
                    'creativity': forms.RadioSelect(),
                    'knowledge_on_company': forms.RadioSelect(),
                    'knowledge_on_industry': forms.RadioSelect(),
                    'evaluation': forms.RadioSelect()}