from django import forms

from .models import Student


class ResultLookupForm(forms.Form):
    admission_number = forms.CharField(max_length=30, label='Admission number')
    date_of_birth = forms.DateField(
        label='Date of birth',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        admission_number = cleaned_data.get('admission_number')
        date_of_birth = cleaned_data.get('date_of_birth')
        if admission_number and date_of_birth:
            student = Student.objects.filter(
                admission_number__iexact=admission_number.strip(),
                date_of_birth=date_of_birth,
            ).first()
            if student is None:
                raise forms.ValidationError('We could not find a student with those details.')
            cleaned_data['student'] = student
        return cleaned_data
