from django.db import models
from uuid import uuid4


class AdmissionApplication(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_UNDER_REVIEW = 'under_review'
	STATUS_ACCEPTED = 'accepted'
	STATUS_REJECTED = 'rejected'

	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pending'),
		(STATUS_UNDER_REVIEW, 'Under review'),
		(STATUS_ACCEPTED, 'Accepted'),
		(STATUS_REJECTED, 'Rejected'),
	]

	application_number = models.CharField(max_length=20, unique=True, editable=False)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=20)
	class_applying_for = models.CharField(max_length=100)
	previous_school = models.CharField(max_length=200, blank=True)
	guardian_name = models.CharField(max_length=200)
	guardian_email = models.EmailField()
	guardian_phone = models.CharField(max_length=30)
	address = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	submitted_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-submitted_at']

	def save(self, *args, **kwargs):
		if not self.application_number:
			self.application_number = f'ADM-{uuid4().hex[:10].upper()}'
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.application_number} - {self.first_name} {self.last_name}'


class Student(models.Model):
	admission_number = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField()
	class_name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def __str__(self):
		return f'{self.admission_number} - {self.first_name} {self.last_name}'


class Subject(models.Model):
	name = models.CharField(max_length=100, unique=True)
	code = models.CharField(max_length=20, unique=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return f'{self.code} - {self.name}'


class Result(models.Model):
	TERM_CHOICES = [
		('first', 'First term'),
		('second', 'Second term'),
		('third', 'Third term'),
	]

	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
	subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='results')
	academic_session = models.CharField(max_length=20, help_text='For example, 2025/2026')
	term = models.CharField(max_length=10, choices=TERM_CHOICES)
	ca_score = models.PositiveSmallIntegerField('Continuous assessment', default=0)
	exam_score = models.PositiveSmallIntegerField(default=0)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['subject__name']
		constraints = [
			models.UniqueConstraint(
				fields=['student', 'subject', 'academic_session', 'term'],
				name='unique_student_subject_term',
			),
		]

	@property
	def total_score(self):
		return self.ca_score + self.exam_score

	@property
	def grade(self):
		total = self.total_score
		if total >= 70:
			return 'A'
		if total >= 60:
			return 'B'
		if total >= 50:
			return 'C'
		if total >= 45:
			return 'D'
		if total >= 40:
			return 'E'
		return 'F'

	@property
	def remark(self):
		return 'Pass' if self.total_score >= 40 else 'Needs improvement'

	def __str__(self):
		return f'{self.student} - {self.subject} ({self.academic_session}, {self.term})'
