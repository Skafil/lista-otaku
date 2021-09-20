from django.test import TestCase
from django.urls import reverse

class BaseTest(TestCase):
    """Klasa wyjściowa z ustawieniami danych do testowania."""
    def setUp(self):
        self.register_url = reverse('register')

        return super().setUp()

class RegisterTest(BaseTest):
    """Test rejestracji."""
    def test_can_view_page_correctly(self):
        """Sprawdź czy strona jest wyświetlana poprawnie."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')