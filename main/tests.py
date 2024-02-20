

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from users.user_models import User
from users.models import UserProfile
from django.http import JsonResponse


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_registration(self):
        post_data = {
            'last_name': 'Doe',
            'first_name': 'John',
            'patronymic': 'Smith',
            'email': 'ermakov.prep@gmail.com',
            'password1': 'adminadmin',
            'password2': 'adminadmin',
            'university_name': '-',
            'post': '-',
            'department': '-',
            'cathedra': '-',
            'phone': '-',
        }
        url = reverse('register')
        response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIsInstance(response, JsonResponse)
        self.assertTrue(response.json()['success'])
        
        # Проверка, что пользователь создан в базе данных
        self.assertTrue(User.objects.filter(email=post_data['email']).exists())
        
        # Проверка, что профиль пользователя создан в базе данных
        user = User.objects.get(email = post_data['email'])
        self.assertTrue(UserProfile.objects.filter(user=user).exists())


    def test_register_view_invalid_data(self):
            # Подготовка неверных данных для POST-запроса
            post_data = {
            'last_name': 'Doe',
            'first_name': 'John',
            'patronymic': 'Smith',
            'email': 'john.doe@example.com',
            'password1': 'test',
            'password2': 'test',
            'university_name': 'Test University',
            'post': 'Test Post',
            'department': 'Test Department',
            'cathedra': 'Test Cathedra',
            'phone': 'двл',
            }
            url = reverse('register')
            # Отправка POST-запроса на представление
            response = self.client.post(url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

            # Проверка, что ответ является JSON-ответом
            self.assertIsInstance(response, JsonResponse)

            # Проверка, что регистрация не успешна
            self.assertFalse(response.json()['success'])

            # Проверка, что в ответе есть ошибки формы
            self.assertIsNotNone(response.json()['errors'])