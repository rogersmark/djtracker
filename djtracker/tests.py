import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from djtracker import models

class IssueViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        seconds = datetime.datetime.now().microsecond
        self.user = User(username="djtracker%s" % seconds, 
            email="djtracker@djtracker.com")
        self.user.set_password('password')
        self.user.save()

    def test_main(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get('/project/default-project/1/')
        
        self.assertEqual(response.status_code, 200)
        
    def test_component(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/component/default-component/')
        
        self.assertEqual(response.status_code, 200)
        
        
