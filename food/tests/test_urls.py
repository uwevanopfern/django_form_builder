from django.test import SimpleTestCase
from django.urls import reverse, resolve
from food.views import login_user, forms, logout_user, home, form_sent, client_details


class TestUrls(SimpleTestCase):

    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).url_name, 'login')
        self.assertEquals(resolve(url).func, login_user)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).url_name, 'logout')
        self.assertEquals(resolve(url).func, logout_user)

    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(resolve(url).url_name, 'home')
        self.assertEquals(resolve(url).func, home)

    def test_forms_url(self):
        url = reverse('forms')
        self.assertEquals(resolve(url).url_name, 'forms')
        self.assertEquals(resolve(url).func, forms)

    def test_form_sent_url(self):
        url = reverse('form.sent')
        self.assertEquals(resolve(url).url_name, 'form.sent')
        self.assertEquals(resolve(url).func, form_sent)
        