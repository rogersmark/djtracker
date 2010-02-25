'''
signals for djtracker

@author: chris vigelius <chris.vigelius@gmx.net>
'''

from django.dispatch import Signal

# sent when an issue has been created
# args:
#   issue    -    the issue which has been created
#   request  -    the request associated with the change (may be None for cron job, shell, ...)
issue_created = Signal(providing_args=[ "issue", "request" ])

# sent when an issue has been updated
# args:
#   issue             the issue which has been updated
#   updated_fields    dict which contains a tuple (oldval, newval) for each changed attribute
issue_updated = Signal(providing_args=[ "issue", "updated_fields", "request" ])

# sent when a comment has been posted for an issue
# args:
#   comment        the comment object
#   issue          the issue object
#   status_change  either None or tuple (old_status, new_status)
issue_commented = Signal(providing_args=[ "comment", "issue", "status_change", "request" ])