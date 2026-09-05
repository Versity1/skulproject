from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdmissionApplicationForm
from .models import AdmissionApplication, Student
from .result_forms import ResultLookupForm


def home(request):
    return render(request, 'home.html')


def apply(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            return redirect('admission_success', application_number=application.application_number)
    else:
        form = AdmissionApplicationForm()
    return render(request, 'admission/apply.html', {'form': form})


def admission_success(request, application_number):
    application = get_object_or_404(
        AdmissionApplication,
        application_number=application_number,
    )
    return render(request, 'admission/success.html', {'application': application})


def result_lookup(request):
    form = ResultLookupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student = form.cleaned_data['student']
        request.session['result_student_id'] = student.id
        return redirect('result_sheet')
    return render(request, 'results/lookup.html', {'form': form})


def result_sheet(request):
    student_id = request.session.get('result_student_id')
    if not student_id:
        return redirect('result_lookup')

    student = get_object_or_404(Student, pk=student_id)
    results = student.results.select_related('subject').all()
    groups = {}
    for result in results:
        groups.setdefault((result.academic_session, result.get_term_display()), []).append(result)
    result_groups = []
    for (academic_session, term), term_results in groups.items():
        total = sum(result.total_score for result in term_results)
        result_groups.append({
            'academic_session': academic_session,
            'term': term,
            'results': term_results,
            'total': total,
            'average': round(total / len(term_results), 2) if term_results else 0,
        })
    return render(request, 'results/sheet.html', {'student': student, 'result_groups': result_groups})


def result_logout(request):
    request.session.pop('result_student_id', None)
    return redirect('result_lookup')