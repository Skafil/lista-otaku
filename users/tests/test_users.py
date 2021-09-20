from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class BaseTest(TestCase):
    """Klasa wyjściowa z ustawieniami danych do testowania."""
    def setUp(self):
        # Ustawienia do RegisterTest.
        self.register_url = reverse('register')
        self.user = {
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password': 'testpassword',
            'password2': 'testpassword',
        }
        self.user_shortpassword = {
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password': 'test',
            'password2': 'test',
        }
        self.user_diffrentpasswords = {
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password': 'testpassword',
            'password2': 'testpassword1',
        }
        self.user_blank_username = {
            'email': 'testemail@gmail.com',
            'username': '',
            'password': 'testpassword',
            'password2': 'testpassword1',
        }

        self.user_blank_email = {
            'email': '',
            'username': 'testusername',
            'password': 'testpassword',
            'password2': 'testpassword1',
        }

        self.user_blank_password = {
            'email': 'testemail@gmail.com',
            'username': 'testusername',
            'password': '',
            'password2': '',
        }

        # Ustawienia do LoginTest.
        self.login_url = reverse('login')

        return super().setUp()

class RegisterTest(BaseTest):
    """Test rejestracji."""
    def test_can_view_page_correctly(self):
        """Sprawdź czy strona jest wyświetlana poprawnie."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_cant_register_with_short_password(self):
        response = self.client.post(self.register_url, self.user_shortpassword, format='text\html')
        self.assertEqual(response.status_code, 200)
    
    def test_cant_register_with_diffrent_passwords(self):
        response = self.client.post(self.register_url, self.user_diffrentpasswords, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_cant_register_with_blank_username(self):
        response = self.client.post(self.register_url, self.user_blank_username, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_cant_register_with_blank_email(self):
        response = self.client.post(self.register_url, self.user_blank_email, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_cant_register_with_blank_password(self):
        response = self.client.post(self.register_url, self.user_blank_password, format='text/html')
        self.assertEqual(response.status_code, 200)

class LoginTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_success(self):
        self.client.post(self.register_url, self.user, format="text/html")
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)
    
    def test_cant_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user, format="text/html")
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_cant_login_with_blank_data(self):
        response = self.client.post(self.login_url, self.user_blank_username, format="text/html")
        self.assertEqual(response.status_code, 200)