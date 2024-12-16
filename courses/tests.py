from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import SystemAdmin, Course, Student, CourseRequest
from django.utils import timezone
import jwt
from django.conf import settings
from courses.views import generate_token


class CourseModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            course_name="Test Course",
            category="programming",
            description="A test course",
            is_active=True
        )

    def test_course_creation(self):
        self.assertEqual(self.course.course_name, "Test Course")
        self.assertEqual(self.course.category, "programming")
        self.assertTrue(self.course.is_active)

class StudentModelTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Test Student",
            number=1234567890,
            email="test@example.com",
            address="123 Test St",
            username="teststudent",
            password="password123"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, "Test Student")
        self.assertEqual(self.student.username, "teststudent")
        self.assertEqual(self.student.email, "test@example.com")

class CourseRequestModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            course_name="Test Course",
            category="programming",
            description="A test course"
        )
        self.student = Student.objects.create(
            name="Test Student",
            number=1234567890,
            email="test@example.com",
            address="123 Test St",
            username="teststudent",
            password="password123"
        )
        self.course_request = CourseRequest.objects.create(
            course=self.course,
            student=self.student,
            reason="Interested in programming"
        )

    def test_course_request_creation(self):
        self.assertEqual(self.course_request.course.course_name, "Test Course")
        self.assertEqual(self.course_request.student.username, "teststudent")
        self.assertEqual(self.course_request.reason, "Interested in programming")

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            course_name="Test Course",
            category="programming",
            description="A test course",
            is_active=True
        )
        self.student = Student.objects.create(
            name="Test Student",
            number=1234567890,
            email="test@example.com",
            address="123 Test St",
            username="teststudent",
            password="password123"
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_all_courses_view(self):
        response = self.client.get(reverse('all_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("courses", response.json())
        self.assertEqual(len(response.json()["courses"]), 1)

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'name': 'New Student',
            'number': '9876543210',
            'email': 'newstudent@example.com',
            'address': '456 Test St',
            'username': 'newstudent',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_login_view(self):
        # Test correct login
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

        # Test incorrect login
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "your password or username is incorrect")

    def test_get_course_view(self):
        response = self.client.get(reverse('get_course'), {'course_id': self.course.course_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["course"]["course_name"], "Test Course")

    def test_create_course_request(self):
        # Generate the token and confirm it's a string
        token = generate_token(self.student.username)
        assert isinstance(token, str), "Token should be a string"
        print(f"Verified token as string: {token}")

        # Set the Authorization header correctly
        self.client.defaults['HTTP_AUTHORIZATION'] = f"Bearer {token}"

        # Execute POST request
        response = self.client.post(reverse('create_course_request'), {
            'course_id': self.course.course_id,
            'reason': 'Want to learn programming'
        })

        # Assert the expected response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")





