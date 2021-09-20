from django.test import TestCase
from otaku_app.models import *

class BaseTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='Test', password="testpassword", email="test@gmail.com")
        self.title = Title.objects.create(name='Black Clover', owner=self.owner)
        self.category = Category.objects.create(name="Anime", owner=self.owner)
        self.subcategory = Subcategory.objects.create(name="Sezon 1", owner=self.owner)

    def test_title_name(self):
        response = self.title
        self.assertEqual('Black Clover', str(response))
    
    def test_category_name(self):
        response = self.category
        self.assertEqual('Anime', str(response))
    
    def test_subcategory_name(self):
        response = self.subcategory
        self.assertEqual('Sezon 1', str(response))