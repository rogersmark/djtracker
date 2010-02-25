'''
models for dynamic reporting

@author: chris vigelius <me@cv.gd>

TODO: support special field {{user}}??? how do i make a query for my worklist???
'''

import re

from django.db import models
from django.contrib.contenttypes.models import ContentType

class Report(models.Model):
    """
    a report
    """
    name = models.CharField(max_length=64, unique=True)    
    content_type = models.ForeignKey(ContentType)
    page_length = models.IntegerField(default=30)
    
    def _kw_for_fcrit(self, fcrit, parameters):
        """
        utility function: evaluate a single filter criterium and return the kw dict 
        """
        kw = {}        
        val_hi = None
        if fcrit.as_param:
            val = parameters[fcrit.value]
            if fcrit.operator == 'range':
                val_hi = parameters[fcrit.value_hi]
        else:
            val = fcrit.value
            if fcrit.operator == 'range':
               val_hi = fcrit.value_hi
    
        if fcrit.operator == 'range':
            kw[str('%s__range' % fcrit.fieldname)] = (val, val_hi)
        else:
            kw[str('%s__%s' % (fcrit.fieldname, fcrit.operator))] = val
        
        return kw
        
    def apply_filters(self, qset, parameters = {}):
        """
        apply filters to qset, returning the resulting qset
        """                        
        # 1. get the union set of all include filters
        qsets = []
        for fcrit in FilterCriterium.objects.filter(report=self, type='I'):
            kw = self._kw_for_fcrit(fcrit, parameters)
            qsets.append(qset.filter(**kw))
        
        if len(qsets)==0:
            qset = qset.all()
        elif len(qsets)==1:
            qset = qsets[0]
        else:
            qset = qsets[0]
            for q in qsets[1:]:
                qset = qset | q                            
        
        # 2. now exclude the excluded fields
        for fcrit in FilterCriterium.objects.filter(report=self, type='E'): 
            kw = self._kw_for_fcrit(fcrit, parameters)
            qset = qset.exclude(**kw)
        
        return qset
        
    def apply_sortcrits(self, qset):
        """
        apply `sortcrits` to `qset`, returning the resulting qset
        """
        args = []
        for crit in SortCriterium.objects.filter(report=self).order_by('index'):
            if crit.order == 'D':                
                args.append('-%s' % crit.fieldname)                
            else:
                args.append('%s' % crit.fieldname)                
        
        return qset.order_by(*args)

    def get_rows(self, parameters = {}, starting_at=None, limit=None):
        qset = self.content_type.model_class().objects
        qset = self.apply_filters(qset, parameters)
        qset = self.apply_sortcrits(qset)
        return qset
    
    def get_row_count(self, parameters = {}):
        qset = self.content_type.model_class().objects
        qset = self.apply_filters(qset, parameters)
        qset = self.apply_sortcrits(qset)
        return qset.count()

#    def apply_columns(self, qset, starting_at=None, limit=None):
#        """
#        get a values dict from qset
#        """
#        args = [ col.fieldname for col in Column.objects.filter(report=self).order_by('index') ]        
#        values = qset.values(*args)
#        if starting_at:            
#            return values[starting_at:limit]
#        else:
#            return values
#    
#    def get_columns(self):
#        """
#        return a list of the columns of this report
#        """
#        if not hasattr(self, '_columns'):
#            self._columns = Column.objects.filter(report=self).order_by('index').values('title', 'fieldname')
#        return self._columns        
#    
#    def _mkrow(self, row):
#        r = []
#        for c in self.get_columns():
#            field = c['fieldname']
#            r.append({'name': field, 'value': row[field]})
#        return r
#    
#    def rows_iter(self, parameters={}, starting_at=None, limit=None):
#        """
#        generator which yields rows, where each row consists of 
#        tuples containing name/value dicts:
#        
#         ...
#         ({'name': 'col1', 'value': 'val1_1'}, {'name': 'col2', 'value': 'val1_2'}),
#         ({'name': 'col1', 'value': 'val2_1'}, {'name': 'col2', 'value': 'val2_2'}),
#         ...        
#        """        
#        print parameters
#        qset = self.content_type.model_class().objects
#        qset = self.apply_filters(qset, parameters)
#        qset = self.apply_sortcrits(qset)
#        rows = self.apply_columns(qset, starting_at, limit)
#        for row in rows:
#            yield self._mkrow(row)
                
TYPE_CHOICES = (('I', 'include'), ('E','exclude'))
OPERATOR_CHOICES =( ('exact', 'equal'), 
                    ('iexact','equal (case ins.)'),
                    ('contains', 'contains'),
                    ('icontains', 'icontains'),
                    #('in', 'in'), # value would be the name of a subquery (not supported yet)
                    ('gt', 'greater than'),
                    ('gte', 'greater or equal'),
                    ('lt', 'less than'),
                    ('lte', 'less or equal'),
                    ('startswith', 'starts with'),
                    ('istartswith', 'starts with (case ins.)'),
                    ('endswith', 'ends with'),
                    ('iendswith', 'ends with (case ins.)'),
                    ('startswith', 'starts with'),
                    ('range', 'between'),
                    ('year', 'year is'),
                    ('month', 'month is'),
                    ('day', 'day is'),
                    ('isnull', 'is null'),
                    ('search', 'full text search'),
                    ('regex', 'regex'),
                    ('iregex', 'iregex'),
                )

class FilterCriterium(models.Model):
    """
    a single filter criterium. each criterium has the following attributes:
     - type: whether it is an 'include' or 'exclude' criterium
     - operator: which operator to use (equal, ...)
     - fieldname: the name of the field we want to compare
     - as_param: whether to interpret the `value` field as dynamic parameter
     - value: the value to compare with
     - value_hi: upper boundary for range 
    """
    report = models.ForeignKey(Report)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    operator = models.CharField(max_length=20, choices=OPERATOR_CHOICES)
    fieldname = models.CharField(max_length=256)
    as_param = models.BooleanField(default=False)
    value = models.CharField(max_length=256)
    value_hi = models.CharField(max_length=256, null=True, blank=True)

ORDER_CHOICES = (('A', 'ascending'), ('D','descending'))
    
class SortCriterium(models.Model):
    """
    a single sort criterium
    """
    report = models.ForeignKey(Report)
    index = models.IntegerField()
    fieldname = models.CharField(max_length=256)
    order = models.CharField(max_length=1, choices=ORDER_CHOICES)

#class Column(models.Model):
#    """
#    a single column definition
#    """
#    report = models.ForeignKey(Report)
#    index = models.IntegerField()
#    title = models.CharField(max_length=256)
#    fieldname = models.CharField(max_length=256)