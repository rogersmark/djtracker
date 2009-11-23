.. DjTracker documentation master file, created by
   sphinx-quickstart on Mon Nov 23 10:54:25 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DjTracker's documentation!
=====================================

Contents:

.. toctree::
   :maxdepth: 2

   projects
   usage

:ref:`search`

Installation Instructions
=====================================

Currently you can clone the `github repository <http://github.com/f4nt/djtracker>`_, or you can always install it via ``pip install djtracker`` (or easy_install if you prefer). Just clone it, and then run "python setup.py build; python setup install". This will install it to your python path. You can then enter the example app path that's included with your clone, and run the following "python manage.py syncdb; python manage runserver" to get up and running

Requirements:

* django-registration - http://bitbucket.org/ubernostrum/django-registration/
* gitpython - http://gitorious.org/git-python

You will need two settings set in your settings.py as well:

* ISSUE_ADDRESS = "user@example.com"
* WEB_SERVER = "apache"

This is the address issue updates will be sent from, and to handle sending files from protected locations. WEB_SERVER can be 'apache' or 'nginx'. The app will default to Apache if left unset. If you do use Apache you will need to install the mod_xsendfile module ( http://tn123.ath.cx/mod_xsendfile/ ). Using this you may run into the issue that /media/attachments/ will be served by Apache regardless, if they go directly to the path of the file where Apache will serve it. This can be circumvented with a directive such as::

        <Directory /var/www/domains/f4ntasmic.com/issues/htdocs/media/attachments/>
                Deny from all
        </Directory>

Django will still be able to get there, but everyday users won't be able to. This will lock it down so that only authenticated users can get to the file. Nginx, much more straight forward. You'll just need the following in your nginx configuration::

    location /protected/ {
        internal;
        alias /PATH/TO/FILES;
    }

Finally youre root urls.py will need the following::

    (r'', include('djtracker.urls')),

Feel free to change the path to suit your needs. I've only tested the application at the root path, but it should work fine at other paths.
