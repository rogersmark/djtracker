'''
unittests for dynamic filter

Created on 15.02.2010

@author: chris vigelius <me@cv.gd>
'''

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model as ModelBase, CharField, DateField, ForeignKey, IntegerField
from datetime import date
from djtracker_reporting.models import Report, FilterCriterium, SortCriterium #, Column

# a simple test data model
class Author(ModelBase):
    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    dob = DateField()    

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

      
class Book(ModelBase):
    author = ForeignKey(Author)
    title = CharField(max_length=64)
    year = IntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.author, self.title)

def create_library():
    """
    create a set of test data
    """
    a=Author(first_name='Robert A.', last_name='Heinlein', dob=date(1907, 07, 07))
    a.save()
    Book(author=a, title='Starship Troopers', year=1959).save()
    Book(author=a, title='Stranger in a Strange Land', year=1961).save()
    Book(author=a, title='Time Enough For Love', year=1973).save()
    Book(author=a, title='Job, A Comedy of Justice', year=1984).save()
    
    a=Author(first_name='Isaac', last_name='Asimov', dob=date(1920, 01, 2))
    a.save()
    Book(author=a, title='I, Robot', year=1950).save()
    Book(author=a, title='Foundation', year=1951).save()
    Book(author=a, title='The Naked Sun', year=1957).save()        
    Book(author=a, title='Nemesis', year=1989).save()
            
    a=Author(first_name='Robert Anton', last_name='Wilson', dob=date(1932, 01, 18))
    a.save()
    Book(author=a, title='The Illuminatus! Trilogy', year=1975).save()
    Book(author=a, title='The Universe Next Door', year=1981).save()
    Book(author=a, title='Prometheus Rising', year=1983).save()        
    Book(author=a, title='The New Inquisition', year=1986).save()
    
class TestReporting(TestCase):
    def setUp(self):        
        create_library()
        self.author_ctype = ContentType.objects.get_for_model(Author)
        self.book_ctype = ContentType.objects.get_for_model(Book)
        self.fnum = 1    
    
    def _get_filter(self, content_type, fcrits=[], as_parameter=False):
        """
        shortcut to get filter easily
        """
        self.fnum += 1
        r = Report(name='test%d' % self.fnum, content_type=content_type)        
        r.save()        
        for fc in fcrits:
            if len(fc)==6:
                FilterCriterium(report=r, type=fc[0], operator=fc[1], fieldname=fc[2], as_param=fc[3], value=fc[4], value_hi=fc[5]).save()
            else:                
                FilterCriterium(report=r, type=fc[0], operator=fc[1], fieldname=fc[2], as_param=fc[3], value=fc[4]).save()
        
        return r
    
    def _get_sortcrits(self, content_type, scrits=[]):        
        self.fnum += 1
        r = Report(name='test%d' % self.fnum, content_type=content_type)
        r.save()        
        for pos, sc in enumerate(scrits):
            SortCriterium(report=r, index=pos, fieldname=sc[0], order=sc[1]).save()
        return r                
    
#    def _get_columns(self, content_type, cols):
#        self.fnum += 1
#        r = Report(name='test%d' % self.fnum, content_type=content_type)
#        r.save()        
#        for pos, col in enumerate(cols):
#            Column(report=r, index=pos, fieldname=col, title='...').save()
#        return r            
    
    def test_filter_exact(self):
        # include single
        r = self._get_filter(self.author_ctype, [('I', 'exact', 'last_name', False, 'Heinlein')])
        result = r.apply_filters(Author.objects)
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0].last_name, 'Heinlein')
        
        # exclude single
        r = self._get_filter(self.author_ctype, [('E', 'exact', 'last_name', False, 'Heinlein')])
        result = r.apply_filters(Author.objects)
        self.assertEquals(len(result), 2)
        for a in result:
            self.assertFalse(a.last_name=='Heinlein')

        # include two
        r = self._get_filter(self.author_ctype, 
                             [('I', 'exact', 'last_name', False, 'Heinlein'),
                              ('I', 'exact', 'last_name', False, 'Asimov')])
        result = r.apply_filters(Author.objects)
        self.assertEquals(len(result), 2)
        for a in result:
            self.assertFalse(a.last_name=='Wilson')
                
        # exclude two
        r = self._get_filter(self.author_ctype, 
                             [('E', 'exact', 'last_name', False, 'Heinlein'),
                              ('E', 'exact', 'last_name', False, 'Asimov')] )
        result = r.apply_filters(Author.objects)
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0].last_name, 'Wilson')
            
    def test_filter_parameters(self):
        heinlein = Author.objects.get(last_name='Heinlein')
        params = {'#1': heinlein}
        r = self._get_filter(self.book_ctype, [('I', 'exact', 'author', True, '#1')])
        result = r.apply_filters(Book.objects, params)
        self.assertEquals(len(result), 4)
        for b in result:
            self.assertEquals(b.author, heinlein)
            
        # to get all the books of Heinlein published before 1973, we need to exclude the opposite
        # (since include filters are ORed)
        # TODO: or should we introduce a method to chain filters???        
        r = self._get_filter(self.book_ctype, [('I', 'exact', 'author',  True,  '#1'),
                                               ('E', 'gte',    'year',   False, 1973) ])
        result = r.apply_filters(Book.objects, params)
        self.assertEquals(len(result), 2)
        for b in result:
            self.assertTrue(b.year < 1973)                
    
    def test_range(self):
        # without parameters
        r = self._get_filter(self.book_ctype, [('I', 'range', 'year',  False,  1970, 1980)])
        result = r.apply_filters(Book.objects)
        self.assertEquals(len(result), 2)
        for b in result:
            self.assertTrue(b.year>=1970)
            self.assertTrue(b.year<=1980)
        
        # with parameters
        r = self._get_filter(self.book_ctype, [('I', 'range', 'year',  True,  '#1', '#2')])
        result = r.apply_filters(Book.objects, {'#1': 1970, '#2': 1980})
        for b in result:
            self.assertTrue(b.year>=1970)
            self.assertTrue(b.year<=1980)        
        
    
    def test_sortcrits(self):
        # all books, ordered by date
        r = self._get_sortcrits(self.book_ctype, [('year','D')])
        result = r.apply_sortcrits(Book.objects)
        year = 2000
        self.assertEquals(len(result), 12)
        for b in result:
            self.assertTrue(b.year < year)
            year = b.year
        
        r = self._get_sortcrits(self.book_ctype, [('author__last_name', 'A'), ('year','D')])
        result = r.apply_sortcrits(Book.objects)
        last_year = 9999
        last_author = '0'        
        for b in result:
            if b.author.last_name != last_author:
                self.assertTrue(b.author.last_name > last_author )
                last_author = b.author.last_name
                last_year = b.year
            self.assertTrue(last_year >= b.year)
            
#    def test_columns(self):
#        r = self._get_columns(self.book_ctype, ('author__last_name', 'title', 'year'))
#        result = r.apply_columns(Book.objects)
#        self.assertEquals(len(result), 12)
#        for b in result:
#            self.assertTrue(b['title'])
#            self.assertTrue(b['year'])
#            self.assertTrue(b['author__last_name'])
                

from django.template import Template, Context

class TestTemplatetag(TestCase):
    def setUp(self):
        create_library()
        r = Report(name='books', content_type=ContentType.objects.get_for_model(Book))
        r.save()
        #Column(report=r, index=0, title='Last Name', fieldname='author__last_name').save()
        #Column(report=r, index=1, title='First Name', fieldname='author__first_name').save()
        #Column(report=r, index=2, title='Title', fieldname='title').save()
        #Column(report=r, index=3, title='Year', fieldname='year').save()
    
    def test_templatetag(self):
        t = Template("""
{% load reporting %}
{% load_report 'books' p1 p2 'foo' as report %}
{{ report }}
        """)
        html = t.render(Context({'p1': 'hello', 'p2': 'world'}))
        self.assertTrue('<tr><td>5</td><td>Isaac Asimov: I, Robot</td></tr>' in html)
        
        
        
