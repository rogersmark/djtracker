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
        
    def test_version(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/version/default-version/')
            
        self.assertEqual(response.status_code, 200)
        
    def test_milestone(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/milestone/default-milestone/')
            
        self.assertEqual(response.status_code, 200)
        
    def test_status(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/status/open/')
            
        self.assertEqual(response.status_code, 200)
        
    def test_priority(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/priority/trivial/')
            
        self.assertEqual(response.status_code, 200)
        
    def test_bugtype(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/type/bug/')
            
        self.assertEqual(response.status_code, 200)
       
    def test_view_id(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/1/')
            
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(
            '/project/default-project/1/?watch=yes')
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(
            '/project/default-project/1/?watch=no')
        self.assertEqual(response.status_code, 302)
        
    def test_view_all(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/view_all/')
            
        self.assertEqual(response.status_code, 200)
        
    def test_view_filtered(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/view_all/?component=default-component&version=default-version&milestone=default-milestone&status=open&type=bug&priority=critical&savename=')
        
        self.assertEqual(response.status_code, 200)
        
    def test_save_filtered(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/view_all/?component=default-component&version=default-version&milestone=default-milestone&status=open&type=bug&priority=critical&save=save&savename=criticals')
            
        self.assertEqual(response.status_code, 200)
        
    def test_submit_modify_issue(self):
        self.client.login(username=self.user.username, password="password")
        post_data = {u'status': [u'1'], 
            u'project': [u'1'], 
            u'name': [u'UnitTest Issue'], 
            u'assigned_to': [u''], 
            u'component': [u'1'], 
            u'created_by': [u'1'], 
            u'priority': [u'1'], 
            u'version': [u'1'],  
            u'issue_type': [u'1'], 
            u'milestone': [u'1'],
            u'description': [u'This is a test.']}
            
        response = self.client.post('/project/default-project/submit_issue/',
            post_data)
        self.assertEqual(response.status_code, 302)
        
        issue = models.Issue.objects.get(name="UnitTest Issue")
        self.assertEqual(issue.description, "This is a test.")
        
        post_data['status'] = [u'2']
        response = self.client.post(
            '/project/default-project/%s/modify_issue/' % issue.id,
            post_data)
        status = models.Status.objects.get(slug="closed")
            
        self.assertEqual(response.status_code, 302)
        issue = models.Issue.objects.get(name="UnitTest Issue")
        self.assertEqual(issue.status, status)
        
    def test_issue_search(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/search/?project=default-project&search=test')
            
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(
            '/project/search/?project=all&search=test')
            
        self.assertEqual(response.status_code, 200)
      
class ProjectViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        seconds = datetime.datetime.now().microsecond
        self.user = User(username="djtracker%s" % seconds, 
            email="djtracker@djtracker.com")
        self.user.set_password('password')
        self.user.save()
        
    def test_index(self):
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        
    def test_project_index(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get('/project/default-project/')
        
        self.assertEqual(response.status_code, 200)
        
class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        seconds = datetime.datetime.now().microsecond
        self.user = User(username="djtracker%s" % seconds, 
            email="djtracker@djtracker.com")
        self.user.set_password('password')
        self.user.save()
        
    def test_view_profile(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/profile/detail/%s/' % self.user.username)
        
        self.assertEqual(response.status_code, 200)
        
    def test_view_dashboard(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/profile/dashboard/')
            
        self.assertEqual(response.status_code, 200)
        
    def test_profile_list(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/profile/list/')
            
        self.assertEqual(response.status_code, 200)
        
    def test_filter_delete(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(
            '/project/default-project/view_all/?component=default-component&version=default-version&milestone=default-milestone&status=open&type=bug&priority=critical&save=save&savename=UnitTestFilter')
            
        self.assertEqual(response.status_code, 200)
        
        issue_filter = models.IssueFilter.objects.get(name='UnitTestFilter')
        response = self.client.get(
            '/profile/filter/delete/%s/' % issue_filter.id)
            
        self.assertEqual(response.status_code, 302)
       
