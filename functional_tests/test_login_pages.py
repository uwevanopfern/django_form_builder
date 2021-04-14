from selenium import webdriver
from food.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestLoginPages(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.user = User.objects.create_superuser(username='uwe', password='fiduciam', email='uwe@example.com')
        self.user.save()

    def tearDown(self):
        self.browser.close()

    def test_heading_h3_text_on_login_page(self):
        self.browser.get(self.live_server_url)
        alert = self.browser.find_element_by_class_name('row')
        self.assertEquals(alert.find_element_by_tag_name('h3').text,'Login')

    def test_login_super_user(self):
        self.client.login(username='uwe', password='fiduciam')
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url + '/admin/')
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh()
        self.browser.get(self.live_server_url + '/admin/')