from datetime import date

from django import forms

from .models import AdmissionApplication


class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'class_applying_for',
            'previous_school',
            'guardian_name',
            'guardian_email',
            'guardian_phone',
            'address',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth >= date.today():
            raise forms.ValidationError('Date of birth must be in the past.')
        return date_of_birth
