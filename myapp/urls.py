from django.urls import path, include

from .views import index, delete, indexx, get_student, deletee, add_student, update_student, addStudent

urlpatterns = [
    path('students/', indexx, name='students'),
    path('home', index, name='index'),
    path('delete/<str:masv>/', delete, name='delete'),
    path('deletee/<str:masv>/', deletee, name='deletee'),
    path('student/<str:masv>/', get_student, name='student_detail'),
    path('add/', add_student, name='add'),
    path('update/', update_student, name='update'),
    path('addstudent/', addStudent, name='addstudent'),
]
