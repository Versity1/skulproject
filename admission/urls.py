from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admissions/apply/', views.apply, name='admission_apply'),
    path(
        'admissions/success/<str:application_number>/',
        views.admission_success,
        name='admission_success',
    ),
    path('results/', views.result_lookup, name='result_lookup'),
    path('results/sheet/', views.result_sheet, name='result_sheet'),
    path('results/logout/', views.result_logout, name='result_logout'),
]
