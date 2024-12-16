from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Course, SystemAdmin, Student,CourseRequest
from django.http import JsonResponse
from django.core import serializers
import json
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import jwt
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

def index(request):
    return render(request, 'index.html')

def course_description_page(request):
    return render(request, 'course_description.html')
def login_page(request):
    return render(request, 'signin.html')
def signup_page(request):
    return render(request, 'register.html')
def profile_page(request):
    return render(request, 'profile.html')
def request_page(request):
    return render(request, 'req.html')


def generate_token(username):
    token = jwt.encode({"username": username}, settings.SECRET_KEY, algorithm="HS256")
    # Convert to string if necessary
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = Student.objects.filter(username=username, password=password)
        if user.exists():
            token = generate_token(username)
            return JsonResponse({"status": "success", "token": token})
        else:
            return JsonResponse({"status": "your password or username is incorrect"})
    return JsonResponse({"status": "error"}, status=400)
        


    

def logout_view(request):
    if request.method=='POST':
        logout(request)
        return JsonResponse({"status": "success"})


        
def enrolled_courses_page(request):
    return render(request, 'enrolled_courses.html')

def all_courses(request):
    courses = Course.objects.filter(is_active=True)
    course_data = []
    for course in courses:
        course_dict = {
            "course_id": course.pk,
            "course_name": course.course_name,
            "category": course.category,
            "description": course.description,
            'is_active': course.is_active,
            "image_url": course.image_url.url  
        }
        course_data.append(course_dict)
    
    for course in course_data:
        course["image_url"] = request.build_absolute_uri(course["image_url"])
    
    return JsonResponse({"courses": course_data})




def student_info(request):
    if request.method=='POST':
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username = payload["username"]
            print(username)
            student = Student.objects.get(username=username)
            course=get_enrolled_courses(username)
            # convert student object to json
            serialized_student = serializers.serialize('json', [student])
            student=json.loads(serialized_student)
            student_data=student[0]['fields']
            return JsonResponse({"student": student_data, "enrolled_courses": course})
        except Exception as e:
            return JsonResponse({"status": "student not found"})


def signup(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            number = request.POST['number']
            email = request.POST['email']
            address = request.POST['address']
            username = request.POST['username']
            password = request.POST['password']

            
            if Student.objects.filter(username=username).exists():
                return JsonResponse({"status": "student already exists"})

            student = Student(
                name=name, number=number, email=email,
                address=address, username=username, password=password
            )
            student.save()

            token = generate_token(username)
            return JsonResponse({"status": "success", "token": token})
        except ValidationError as e:
            return JsonResponse({"status": "error", "message": str(e)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error"}, status=400)
        
def get_course_request(request):
    course_requests = CourseRequest.objects.all().filter(student_id=1)
    return JsonResponse({"course_requests": list(course_requests.values())})


def get_course(request):
    if request.method=='GET':
        course_id = request.GET['course_id']
        
        print(course_id)
        course = Course.objects.get(course_id=course_id)
        course_data = {
            "course_id": course.pk,
            "course_name": course.course_name,
            "category": course.category,
            "description": course.description,
            "image_url": course.image_url.url  
        }
        course_data["image_url"] = request.build_absolute_uri(course_data["image_url"])

        return JsonResponse({"course": course_data})
    


def create_course_request(request):
    if request.method=='POST':
        course_id = request.POST['course_id']
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1]
        username = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])["username"]
        student_id = Student.objects.get(username=username).pk
        reason = request.POST['reason']
        course = Course.objects.get(course_id=course_id)
        

        course_request = CourseRequest(course=course,student_id=student_id,reason=reason)

        student = Student.objects.get(username=username)
        student.enrolled_courses.add(course)
        try:
            if CourseRequest.objects.filter(course=course,student_id=student_id):
                return JsonResponse({"status": "request already exist"})
            course_request.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": e})
        
def get_enrolled_courses(usename):
    student = Student.objects.get(username=usename)
    enrolled_courses = student.enrolled_courses.all()
    course_data = []
    for course in enrolled_courses:
        course_dict = {
            "course_id": course.pk,
            "course_name": course.course_name,
        }
        course_data.append(course_dict)
    return course_data

        
        