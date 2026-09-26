from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import inlineformset_factory
from .models import User, JobSeekerProfile, Education, WorkExperience, Project, Link

class CustomUserCreationForm(UserCreationForm):
    company_name = forms.CharField(max_length=200, required=False,
        label='Company name (recruiters only)',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    field_order = ['username', 'email', 'role', 'company_name', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'role']
        widgets = {'role': forms.Select(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].required = True

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('role') == User.Role.RECRUITER and not cleaned_data.get('company_name'):
            self.add_error('company_name', 'Recruiters must enter a company name.')
        return cleaned_data

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['headline', 'show_headline', 'location', 'show_location',
            'skills', 'show_skills', 'show_education', 'show_experience',
            'show_projects', 'show_links']
        widgets = {'skills': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super(JobSeekerProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name.startswith('show_'):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif name != 'skills':
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