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
    
# pickledobjectfield
# taken from http://www.djangosnippets.org/snippets/1694/
    
from copy import deepcopy
from base64 import b64encode, b64decode
from zlib import compress, decompress
try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

from django.db import models
from django.utils.encoding import force_unicode

class PickledObject(str):
    """
    A subclass of string so it can be told whether a string is a pickled
    object or not (if the object is an instance of this class then it must
    [well, should] be a pickled one).
    
    Only really useful for passing pre-encoded values to ``default``
    with ``dbsafe_encode``, not that doing so is necessary. If you
    remove PickledObject and its references, you won't be able to pass
    in pre-encoded values anymore, but you can always just pass in the
    python objects themselves.
    
    """
    pass

def dbsafe_encode(value, compress_object=False):
    """
    We use deepcopy() here to avoid a problem with cPickle, where dumps
    can generate different character streams for same lookup value if
    they are referenced differently. 
    
    The reason this is important is because we do all of our lookups as
    simple string matches, thus the character streams must be the same
    for the lookups to work properly. See tests.py for more information.
    """
    if not compress_object:
        value = b64encode(dumps(deepcopy(value)))
    else:
        value = b64encode(compress(dumps(deepcopy(value))))
    return PickledObject(value)

def dbsafe_decode(value, compress_object=False):
    if not compress_object:
        value = loads(b64decode(value))
    else:
        value = loads(decompress(b64decode(value)))
    return value

class PickledObjectField(models.Field):
    """
    A field that will accept *any* python object and store it in the
    database. PickledObjectField will optionally compress it's values if
    declared with the keyword argument ``compress=True``.
    
    Does not actually encode and compress ``None`` objects (although you
    can still do lookups using None). This way, it is still possible to
    use the ``isnull`` lookup type correctly. Because of this, the field
    defaults to ``null=True``, as otherwise it wouldn't be able to store
    None values since they aren't pickled and encoded.
    
    """
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        self.compress = kwargs.pop('compress', False)
        self.protocol = kwargs.pop('protocol', 2)
        kwargs.setdefault('null', True)
        kwargs.setdefault('editable', False)
        super(PickledObjectField, self).__init__(*args, **kwargs)
    
    def get_default(self):
        """
        Returns the default value for this field.
        
        The default implementation on models.Field calls force_unicode
        on the default, which means you can't set arbitrary Python
        objects as the default. To fix this, we just return the value
        without calling force_unicode on it. Note that if you set a
        callable as a default, the field will still call it. It will
        *not* try to pickle and encode it.
        
        """
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        # If the field doesn't have a default, then we punt to models.Field.
        return super(PickledObjectField, self).get_default()

    def to_python(self, value):
        """
        B64decode and unpickle the object, optionally decompressing it.
        
        If an error is raised in de-pickling and we're sure the value is
        a definite pickle, the error is allowed to propogate. If we
        aren't sure if the value is a pickle or not, then we catch the
        error and return the original value instead.
        
        """
        if value is not None:
            try:
                value = dbsafe_decode(value, self.compress)
            except:
                # If the value is a definite pickle; and an error is raised in
                # de-pickling it should be allowed to propogate.
                if isinstance(value, PickledObject):
                    raise
        return value

    def get_db_prep_value(self, value):
        """
        Pickle and b64encode the object, optionally compressing it.
        
        The pickling protocol is specified explicitly (by default 2),
        rather than as -1 or HIGHEST_PROTOCOL, because we don't want the
        protocol to change over time. If it did, ``exact`` and ``in``
        lookups would likely fail, since pickle would now be generating
        a different string. 
        
        """
        if value is not None and not isinstance(value, PickledObject):
            # We call force_unicode here explicitly, so that the encoded string
            # isn't rejected by the postgresql_psycopg2 backend. Alternatively,
            # we could have just registered PickledObject with the psycopg
            # marshaller (telling it to store it like it would a string), but
            # since both of these methods result in the same value being stored,
            # doing things this way is much easier.
            value = force_unicode(dbsafe_encode(value, self.compress))
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def get_internal_type(self): 
        return 'TextField'
    
    def get_db_prep_lookup(self, lookup_type, value):
        if lookup_type not in ['exact', 'in', 'isnull']:
            raise TypeError('Lookup type %s is not supported.' % lookup_type)
        # The Field model already calls get_db_prep_value before doing the
        # actual lookup, so all we need to do is limit the lookup types.
        return super(PickledObjectField, self).get_db_prep_lookup(lookup_type, value) 