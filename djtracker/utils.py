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

