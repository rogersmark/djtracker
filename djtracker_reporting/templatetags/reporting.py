'''
templatetags for reporting

Created on 23.02.2010

@author: chris vigelius <me@cv.gd>
'''

from django import template
from django.template import resolve_variable
from django.template.loader import select_template
from djtracker_reporting import models

class ReportVar:
    """
    class for the context variable which represents a report 
    """
    def __init__(self, context, report_name, args, user):
        self.context = context
        self.report_name = report_name
        self.report = models.Report.objects.get(name=report_name)
        #self.columns = list(self.report.get_columns())
        params = {'user': user}
        for pos, arg in enumerate(args):
            params['p%d' % pos] = arg
        self.rows = self.report.get_rows(params)
        self.row_count = self.report.get_row_count(params)
    
    def __unicode__(self):
        # TODO: use the 'report.html' template to render the report
        # it will consist of a <table><tr>{% include header %}</tr>{% for row report.rows %}...                         
        t = select_template(['djtracker_reporting/report_%s.html' % self.report_name, 
                                    'djtracker_reporting/report.html'])        
        self.context.push()
        self.context['report'] = self
        html = t.render(self.context)
        self.context.pop()
        return html

class ReportNode(template.Node):
    """
    template node for the record. this will simply add an instance of ReportVar 
    to the context.
    """
    def __init__(self, report_name, var_name, args):
        self.report_name = report_name
        self.var_name = var_name
        self.args = args

    def render(self, context):
        try:
            request = resolve_variable('request', context)
        except:
            request = None
        
        context.update({self.var_name: ReportVar(context,
                                                 resolve_variable(self.report_name, context), 
                                                 [resolve_variable(arg, context) for arg in self.args], 
                                                 request.user if request else None)})
        return ''
    
register = template.Library()

@register.tag
def load_report(parser, token):
    try:
        bits = list(token.split_contents())            
        tagname = bits.pop(0)
        reportname = bits.pop(0)
        args = []
        while True:
            arg = bits.pop(0)
            if arg=='as':
                break
            args.append(arg)
        varname = bits.pop(0)
    except ValueError:
        raise template.TemplateSyntaxError, "%r syntax: [p1 [p2 [...]]] as varname" % tagname

    return ReportNode(reportname, varname, args)
