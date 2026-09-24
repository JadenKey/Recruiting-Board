from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description', 'location', 'salary_min',
            'salary_max', 'workplace', 'visa_sponsorship', 'skills']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'visa_sponsorship':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
