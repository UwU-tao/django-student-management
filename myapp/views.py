from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Student
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import StudentSerializer
from .forms import StudentForm
from datetime import datetime

def index(request):
    data = Student.objects.all()
    data_with_increment = []
    for index, item in enumerate(data, start=1):
        item_with_increment = {'increment': index, 'data': item}
        data_with_increment.append(item_with_increment)
    return render(request, 'index.html', {'students': data_with_increment})

def indexx(request):
    data = Student.objects.all()
    data_with_increment = []
    for index, item in enumerate(data, start=1):
        item_with_increment = {'increment': index, 'data': serializers.serialize('python', [item])[0]}
        data_with_increment.append(item_with_increment)
    return JsonResponse({'students': data_with_increment})

@csrf_exempt
def delete(request, masv):
    if request.method == 'DELETE':
        try:
            student = Student.objects.get(masv=masv)
            student.delete()
            return JsonResponse({'message': 'Student deleted successfully.'}, status=204)
        except Student.DoesNotExist:
            return JsonResponse({'message': 'Student does not exist.'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

def deletee(request, masv):
    student = Student.objects.get(masv=masv)
    if request.method == 'POST':
        student.delete()
        index(request)
        return redirect('/home')
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
    

@api_view(['GET'])
def get_student(request, masv):
    try:
        student = Student.objects.get(masv=masv)
        serializer = StudentSerializer(student)
        return JsonResponse(serializer.data, status=200)
    except Student.DoesNotExist:
        return JsonResponse({'message': 'Student not found.'}, status=404)

@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # return JsonResponse(serializer.data, status=201)
        return JsonResponse({'message': 'Student added successfully.'})
    return JsonResponse({'message': 'Student already existed.'})

def update_student(request):
    if request.method == 'POST':
        student_id = request.POST['idInput']
        name = request.POST['nameInput']
        dob = request.POST['dobInput']
        hometown = request.POST['htInput']
        
        student = Student.objects.get(masv=student_id)

        # Update the student attributes
        student.hoten = name
        student.ngaysinh = dob
        student.quequan = hometown
        student.save()

        # Redirect to the student detail page or any other appropriate page
        return redirect('/home')


def addStudent(request):
    if request.method == 'POST':
        student_id = request.POST['idInput']
        name = request.POST['nameInput']
        dob = request.POST['dobInput']
        hometown = request.POST['htInput']
        
        if student_id and name and dob and hometown:
            dob_datetime = datetime.strptime(dob, '%Y-%m-%d')
            if dob_datetime > datetime.now():
                return JsonResponse({'success': False, 'error': 'Invalid date of birth'})
            
            if len(student_id) != 8:
                return JsonResponse({'success': False, 'error': 'Invalid student ID length'})
            
            student = Student(masv=student_id, hoten=name, ngaysinh=dob, quequan=hometown)
            student.save()
            return JsonResponse({'success': True, 'student_id': student.masv})
        
        else:
            return JsonResponse({'success': False, 'error': 'Incomplete data'})
        
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

