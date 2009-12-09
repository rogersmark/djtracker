from django import template
from django.db.models import get_model
from django.template import resolve_variable

from djtracker import utils

register = template.Library()

class ModelObjectNode(template.Node):
    """
    TODO: Documentation
    """
    def __init__(self, app_name, model_name, sort, count, var_name):
        self.app_name = app_name
        self.model_name = model_name
        self.sort = sort
        self.count = int(count)
        self.var_name = var_name

    def render(self, context):
        try:
            request = resolve_variable('request', context)
        except:
            request = None
        try:
            model = get_model(self.app_name, self.model_name)
        except:
            raise TemplateSyntaxError, "Failed to retrieve model"
        
        if hasattr(model.objects, 'filter_allowed'):
            object_list = model.objects.filter_allowed(request)
        else:
            object_list = model.objects.all()
        
        object_list = object_list.order_by(self.sort)
        if object_list.count() > self.count:
            object_list = object_list[:self.count]
                        
        context.update({self.var_name: object_list})
        return ''

@register.tag
def get_object_models(parser, token):
    """
    USAGE:
    {% load get_objects %}
      {% get_object_models "APP_NAME" "MODEL_NAME" "SORT" "NUMBER OF ITEMS" "VARIABLE_NAME"
      Then iterate through

    EXAMPLE:
    {% load get_objects %}
      {% get_object_models "django_yaba" "Story" "-created" "3" "blog_posts" %}
        <ul>
        {% if blog_posts %}
          {% for post in blog_posts %}
            <li><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></li>
          {% endfor %}
        {% endif %}
    """
    try:
        tag_name, app_name, model_name, sort, count, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Object Tag requires 5 variables")

    return ModelObjectNode(app_name[1:-1], model_name[1:-1], sort[1:-1], count[1:-1], var_name[1:-1])
