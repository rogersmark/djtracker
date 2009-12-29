def check_permissions(permission_type, user, project):
    """
    Here we check permission types, and see if a user has proper perms.
    If a user has "edit" permissions on a project, they pretty much have
    carte blanche to do as they please, so we kick that back as true. 
    Otherwise we go more fine grained and check their view and comment 
    permissions
    """
    try:
        groups = user.groups.all()
    except AttributeError:
        groups = None
    if user in project.users_can_edit.all():
        return True
    
    for x in groups:
        if x in project.groups_can_edit.all():
            return True
            
    if permission_type == "edit":
        if project.allow_anon_editing:
            return True

    if permission_type == "view":
        if user in project.users_can_view.all():
            return True

        for x in groups:
            if x in project.groups_can_view.all():
                return True

        if project.allow_anon_viewing is True:
            return True

    if permission_type == "comment":
        if user in project.users_can_comment.all():
            return True

        for x in groups:
            if x in project.groups_can_comment.all():
                return True

        if project.allow_anon_comment is True:
            return True

    ## If we make it all the way here, we haven't returned True yet.
    ## Thus we'll kick back false on the fall through
    return False

def check_perms(request, project, user=None):
    """
    Here we check permission types, and see if a user has proper perms.
    If a user has "edit" permissions on a project, they pretty much have
    carte blanche to do as they please, so we kick that back as true. 
    Otherwise we go more fine grained and check their view and comment 
    permissions
    """
    can_view = False
    can_edit = False
    can_comment = False
    if request is not None:
        user = request.user
    else:
        user = user

    try:
        groups = user.groups.all()
    except AttributeError:
        groups = None

    try:
        if user.is_authenticated():
            if project.allow_authed_viewing:
                can_view = True
            if project.allow_authed_editing:
                can_edit = True
                can_view = True
                can_comment = True
            if project.allow_authed_comment:
                can_comment = True
                can_view = True
            if user in project.users_can_view.all():
                can_view = True
            if user in project.users_can_edit.all():
                can_edit = True
                can_comment = True
                can_view = True
            if user in project.users_can_comment.all():
                can_comment = True
                can_view = True

            for x in groups:
                if x in project.groups_can_view.all():
                    can_view = True
                if x in project.groups_can_edit.all():
                    can_edit = True
                    can_comment = True
                    can_view = True
                if x in project.users_can_comment.all():
                    can_comment = True
                    can_view = True
    except AttributeError:
        pass

    if project.allow_anon_viewing:
        can_view = True
    if project.allow_anon_editing:
        can_edit = True
    if project.allow_anon_comment:
        can_comment = True

    return can_view, can_edit, can_comment

# ported snipped from another project
from django.core.mail import EmailMessage, EmailMultiAlternatives #, SMTPConnection
from django.template.loader import get_template
from django.template.loader_tags import BlockNode

class MailTemplate:
    """
    extended mail template processor which uses top-level blocks to
    describe the various parts of a mail:
    
    {% block subject %}Hello World{% endblock %}
    
    {% block body %}
    this is the mail body
    {% endblock %}
    
    {% block html_body %}
    <html><body><h1>this is the mail body</body></html>
    {% endblock %}
    
    It is recommended, but not required that mail templates are saved with extension ".mail"
    
    supported block names are
    subject       (required)    Subject of the mail
    body          (required)    Mail body
    body_html     (optional)    HTML Body. If present, mail will be multipart/html
    
    """
    def __init__(self, template_name):
        self.template = get_template(template_name)
        self.mailparts = dict((node.name, node) for node in self.template.nodelist.get_nodes_by_type(BlockNode))
    
    def render(self, part, context):
        """
        render a mail part
        """
        try:
            return self.mailparts[part].nodelist.render(context)
        except KeyError:
            return None
        
    def render_to_mail(self, context):
        """
        render template content to ``EmailMessage`` object 
        """ 
        if 'body_html' in self.mailparts:
            msg = EmailMultiAlternatives(subject=self.render('subject', context), 
                                         body=self.render('body', context))
            msg.attach_alternative(self.render('body_html', context), "text/html")
        else:
            msg = EmailMessage(subject=self.render('subject', context), 
                               body=self.render('body', context))
        return msg 