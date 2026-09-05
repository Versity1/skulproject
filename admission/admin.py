from django.contrib import admin

from .models import AdmissionApplication, Result, Student, Subject


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
	list_display = (
		'application_number',
		'applicant_name',
		'class_applying_for',
		'status',
		'submitted_at',
	)
	list_filter = ('status', 'class_applying_for', 'submitted_at')
	search_fields = (
		'application_number',
		'first_name',
		'last_name',
		'guardian_email',
	)
	readonly_fields = ('application_number', 'submitted_at', 'updated_at')

	@admin.display(description='Applicant')
	def applicant_name(self, application):
		return f'{application.first_name} {application.last_name}'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('admission_number', 'full_name', 'class_name', 'date_of_birth')
	search_fields = ('admission_number', 'first_name', 'last_name')

	@admin.display(description='Student')
	def full_name(self, student):
		return f'{student.first_name} {student.last_name}'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ('code', 'name')
	search_fields = ('code', 'name')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
	list_display = ('student', 'subject', 'academic_session', 'term', 'total_score', 'grade')
	list_filter = ('academic_session', 'term', 'subject')
	search_fields = ('student__admission_number', 'student__first_name', 'student__last_name')
