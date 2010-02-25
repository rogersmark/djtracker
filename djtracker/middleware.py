'''
global request middleware: provides a global request object for usage in models, signals etc.  

@author: unknown, source can be found in various places on the web
'''

try:
     from threading import local
except ImportError:
     # Fallback for Python 2.3
     from django.utils._threading_local import local

# this is a global variable, so the name should be as unique as possible,
# to avoid interference with other globals
GLOBAL_REQUEST_ATTR_NAME = '_djtracker_global_request'

thread_namespace = local()

class GlobalRequestMiddlewareException(Exception):
    """
    a problem with GlobalRequestMiddleware
    """
    pass

class GlobalRequestMiddleware:
    """
    GlobalRequestMiddleware provides a global request object storage,
    which can be used to determine currently logged on user, client IP
    and other information.    
    """
    def process_request(self, request):
        # set the current request in thread namespace
        setattr(thread_namespace, GLOBAL_REQUEST_ATTR_NAME, request)
        
    def process_response(self, request, response):
        # clear the request
        try:
            delattr(thread_namespace, GLOBAL_REQUEST_ATTR_NAME)
        except AttributeError:
            pass
        return response

def get_current_request(fail_silently=False):
    if not hasattr(thread_namespace, GLOBAL_REQUEST_ATTR_NAME):
        if fail_silently:
            return None
        else:
            raise GlobalRequestMiddlewareException('request not found in thread_namespace. Did you add "djtracker.middleware.GlobalRequestMiddleware" to SETTINGS.MIDDLEWARE_CLASSES ?')
    return getattr(thread_namespace, GLOBAL_REQUEST_ATTR_NAME, None)