import datetime

from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.conf import settings

from djtracker import models, utils
from djtracker_comments.models import CommentWithIssueStatus as Comment

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
        
    def test_view_submit_issue(self):
        self.client.login(username=self.user.username, password='password')
        
        response = self.client.get('/project/default-project/submit_issue/')
        self.assertEqual(response.status_code, 200)
        
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
        
class FeedTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        seconds = datetime.datetime.now().microsecond
        self.user = User(username="djtracker_feed%s" % seconds,
            email="djtracker@djtracker_feed.com")
        self.user.set_password('password')
        self.user.save()
        
    def test_personal_feed(self):
        response = self.client.get('/feeds/personal/%s/%s/' % (self.user.id,
         self.user.userprofile.uuid))
        
        self.assertEqual(response.status_code, 200)
        
    def test_project_feed(self):
        response = self.client.get('/feeds/project/1/')
        
        self.assertEqual(response.status_code, 200)
        
    def test_failed_personal_feed(self):
        response = self.client.get('/feeds/personal/%s/%s/' % (self.user.id, 
            self.user.userprofile.uuid[0:-2]))
            
        self.assertEqual(response.status_code, 404)
        
    def test_failed_project_feed(self):
        response = self.client.get('/feeds/project/123414/')
        
        self.assertEqual(response.status_code, 404)
        
class SignalTest(TestCase):

    def setUp(self):
        self.client = Client()
        seconds = datetime.datetime.now().microsecond
        self.user = User(username="djtracker%s" % seconds, 
            email="djtracker@djtracker.com")
        self.user.set_password('password')
        self.user.save()
        
    
    def test_comment_post_save(self):
        content_type = ContentType.objects.get(model='issue')
        comment = Comment()
        comment.user_name = self.user.username
        comment.user_email = self.user.email
        comment.content_type = content_type
        comment.object_pk = 1
        comment.comment = "This is a test comment"
        comment.site = Site.objects.get(id=settings.SITE_ID)
        comment.save()

class NotificationTest(TestCase):
    fixtures = ['testdata/00_test_users.json', 'testdata/01_test_config.json']
    recipient_list = ['processor@djtracker.corp', 'watcher@djtracker.corp', 'creator@djtracker.corp']    
        
    def test_notify_on_create_issue(self):
        # create some issue
        issue = models.Issue()
        issue.name = "new issue"
        issue.project = models.Project.objects.get(pk=1)
        issue.status = models.Status.objects.get(slug='test-open')
        issue.issue_type = models.IssueType.objects.get(slug='bug')
        issue.priority = models.Priority.objects.get(slug='test-normal')
        issue.description = "a new issue"
        issue.assigned_to = models.UserProfile.objects.get(pk=3)
        issue.created_by = models.UserProfile.objects.get(pk=2)
        issue.save()

        self.assertEquals(len(mail.outbox), 3)
        self.check_outbox(['processor@djtracker.corp', 'creator@djtracker.corp'], "DjTracker: [unittest-project]: New Issue #2 submitted", "Status:   Open")                
    
    def test_notify_on_change_issue(self):
        # change some issue
        issue = models.Issue.objects.get(pk=1)
        issue.status = models.Status.objects.get(slug='test-closed')
        issue.save()
        
        self.assertEquals(len(mail.outbox), 3)
        self.check_outbox(self.recipient_list, "DjTracker: [unittest-project]: Issue #1 updated", "Status:   Closed")                
    
    def test_notify_on_comment(self):
        # post some comment
        comment = Comment()
        content_type = ContentType.objects.get(model='issue')
        comment = Comment()
        comment.user_name = 'somebody'
        comment.user_email = 'somebody@some.site'
        comment.content_type = content_type
        comment.object_pk = 1
        comment.comment = "This is a test comment"
        comment.site = Site.objects.get(id=settings.SITE_ID)
        comment.save()
        
        self.assertEquals(len(mail.outbox), 3)        
        self.check_outbox(self.recipient_list, "DjTracker: [unittest-project]: New Comment on Issue #1 by somebody", comment.comment)        
    
    def check_outbox(self, recipient_list, subject, body_part):
        """test outbox for notifications"""
        actual_recipients = []
        for msg in mail.outbox:
            self.assertEquals(msg.subject, subject)
            self.assertTrue(body_part in msg.body)
            actual_recipients.append(msg.to[0])
        for r in recipient_list:
            self.assertTrue(r in actual_recipients)

class CheckUtils(TestCase):
    
    def setUp(self):
        seconds = datetime.datetime.now().microsecond
        self.user = User(username="djtracker_utils%s" % seconds,
            email="djtracker_utils@djtracker.com")
        self.user.save()
        self.project = models.Project.objects.get(id=1)
        self.project.allow_anon_comment = False
        self.project.allow_anon_viewing = False
        self.project.allow_anon_editing = False
        self.project.save()
        
    def test_check_permissions_false(self):
        can_comment = utils.check_permissions('comment', self.user, self.project)
        can_view = utils.check_permissions('view', self.user, self.project)
        can_edit = utils.check_permissions('edit', self.user, self.project)
        
        self.assertEqual(can_comment, False)
        self.assertEqual(can_view, False)
        self.assertEqual(can_edit, False)
        
    def test_check_permissions_true(self):
        self.project.allow_anon_comment = True
        self.project.allow_anon_viewing = True
        self.project.allow_anon_editing = True
        self.project.save()
        
        can_comment = utils.check_permissions('comment', self.user, self.project)
        can_view = utils.check_permissions('view', self.user, self.project)
        can_edit = utils.check_permissions('edit', self.user, self.project)
        
        self.assertEqual(can_comment, True)
        self.assertEqual(can_view, True)
        self.assertEqual(can_edit, True)       