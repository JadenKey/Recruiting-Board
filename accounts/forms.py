from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import inlineformset_factory
from .models import User, JobSeekerProfile, Education, WorkExperience, Project, Link
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'role']
        widgets = {'role': forms.Select(attrs={'class': 'form-control'})}
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['headline', 'location', 'skills']

    def __init__(self, *args, **kwargs):
        super(JobSeekerProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProfileEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEntryForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

date_widget = forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})

EducationFormSet = inlineformset_factory(JobSeekerProfile, Education, form=ProfileEntryForm,
    fields=['school', 'degree', 'field_of_study', 'start_date', 'end_date'],
    widgets={'start_date': date_widget, 'end_date': date_widget}, extra=1)
WorkExperienceFormSet = inlineformset_factory(JobSeekerProfile, WorkExperience, form=ProfileEntryForm,
    fields=['title', 'company', 'description', 'start_date', 'end_date'],
    widgets={'start_date': date_widget, 'end_date': date_widget}, extra=1)
ProjectFormSet = inlineformset_factory(JobSeekerProfile, Project, form=ProfileEntryForm,
    fields=['title', 'description'], extra=1)
LinkFormSet = inlineformset_factory(JobSeekerProfile, Link, form=ProfileEntryForm,
    fields=['label', 'url'], extra=1)