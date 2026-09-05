from django.test import TestCase

from datetime import date, timedelta

from .models import AdmissionApplication, Result, Student, Subject


class AdmissionApplicationWorkflowTests(TestCase):
	valid_data = {
		'first_name': 'Ada',
		'last_name': 'Lovelace',
		'date_of_birth': '2012-12-10',
		'gender': 'Female',
		'class_applying_for': 'Year 8',
		'previous_school': 'Green School',
		'guardian_name': 'Charles Lovelace',
		'guardian_email': 'charles@example.com',
		'guardian_phone': '08000000000',
		'address': '1 Academy Road',
	}

	def test_application_form_submission_creates_pending_application(self):
		response = self.client.post('/admissions/apply/', self.valid_data)

		application = AdmissionApplication.objects.get()
		self.assertRedirects(
			response,
			f'/admissions/success/{application.application_number}/',
		)
		self.assertTrue(application.application_number.startswith('ADM-'))
		self.assertEqual(application.status, AdmissionApplication.STATUS_PENDING)

	def test_future_date_of_birth_is_rejected(self):
		data = {**self.valid_data, 'date_of_birth': date.today() + timedelta(days=1)}

		response = self.client.post('/admissions/apply/', data)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Date of birth must be in the past.')
		self.assertEqual(AdmissionApplication.objects.count(), 0)


class ResultPortalTests(TestCase):
	def setUp(self):
		self.student = Student.objects.create(
			admission_number='STU-001',
			first_name='Ada',
			last_name='Lovelace',
			date_of_birth='2012-12-10',
			class_name='Year 8',
		)
		mathematics = Subject.objects.create(name='Mathematics', code='MATH')
		Result.objects.create(
			student=self.student,
			subject=mathematics,
			academic_session='2025/2026',
			term='first',
			ca_score=25,
			exam_score=65,
		)

	def test_valid_lookup_redirects_to_result_sheet(self):
		response = self.client.post('/results/', {
			'admission_number': 'stu-001',
			'date_of_birth': '2012-12-10',
		})

		self.assertRedirects(response, '/results/sheet/')
		sheet = self.client.get('/results/sheet/')
		self.assertContains(sheet, 'Mathematics')
		self.assertContains(sheet, '90')
		self.assertContains(sheet, 'A')

	def test_result_sheet_requires_lookup(self):
		response = self.client.get('/results/sheet/')

		self.assertRedirects(response, '/results/')
