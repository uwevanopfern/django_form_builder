from django.test import TestCase, Client
from django.urls import reverse
from food.models import User


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_new(username='uwe', password='fiduciam', email='uwe@example.com')
        self.user.save()

    def test_correct_user_created(self):
        self.assertEquals(self.user.username, 'uwe')

    def test_wrong_user_created(self):
        self.assertNotEquals(self.user.username, 'aime')