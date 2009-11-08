from djtracker import models

def check_permissions(permission_type, user, project):
    """
    Here we check permission types, and see if a user has proper perms.
    If a user has "edit" permissions on a project, they pretty much have
    carte blanche to do as they please, so we kick that back as true. 
    Otherwise we go more fine grained and check their view and comment 
    permissions
    """
    groups = user.groups.all()
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
