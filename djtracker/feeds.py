from djtracker import models

from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

class LatestIssues(Feed):
    title = "Recently Updated Issues"
    description = "All issues recently commented on, or updated in your DjTracker instance"
    link = ""
    
    def items(self):
        return models.Issue.objects.filter_allowed(self.request)
        
class PersonalFeed(Feed):
    title_template = "djtracker/feeds/personal_feed_title.html"
    description_template = "djtracker/feeds/personal_feed_description.html"
    def get_object(self, bits):
        print bits
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return models.UserProfile.objects.get(id=bits[0])

            
    def title(self, obj):
        return "Feed for %s" % obj
        
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        else:
            return obj.get_absolute_url()
        
    def description(self, obj):
        return "Recent issues for %s" % obj
        
    def items(self, obj):
        user_issues = []
        for x in obj.issue_creator.all():
            if x.id not in user_issues:
                user_issues.append(x.id)
                
        for x in obj.issue_set.all():
            if x.id not in user_issues:
                user_issues.append(x.id)
                
        for x in obj.watched_set.all():
            if x.id not in user_issues:
                user_issues.append(x.id)
                
        return models.Issue.objects.filter(id__in=user_issues).order_by('-modified_date')