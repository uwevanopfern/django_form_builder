from django.test import TestCase, Client
from django.urls import reverse
from food.models import User
import json
from django.contrib.auth import authenticate, login, logout


class TestView(TestCase):

    def setUp(self):
        self.user = User.objects.create_new(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_login_with_correct_credentials(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_login_with_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_login_with_wrong_password(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_forms_GET(self):
        client = Client()
        response = client.get(reverse('forms'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/forms.html')

    def test_form_sent_GET(self):
        client = Client()
        response = client.get(reverse('form.sent'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/form_sent.html')