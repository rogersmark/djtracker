'''
Created on 15.02.2010

@author: chris vigelius <me@cv.gd>
'''

from django.contrib import admin
from djtracker_reporting import models

class FilterCriteriumInline(admin.TabularInline):
    model = models.FilterCriterium

class SortCriteriumInline(admin.TabularInline):
    model = models.SortCriterium

#class ColumnInline(admin.TabularInline):
#    model = models.Column

class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type']
    inlines = [SortCriteriumInline, FilterCriteriumInline]
    
admin.site.register(models.Report, ReportAdmin)
