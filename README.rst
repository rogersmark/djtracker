==========
DjTracker
==========
Application Name - DjTracker
Author - Mark Rogers (f4nt)
License - BSD License

Demo at http://issues.f4ntasmic.com

------------------------
DjTracker Introduction:
------------------------

DjTracker is meant to be an issue tracker built with Python and Django. I hadn't personally seen an active one that suited my needs, so I set out to build this. Trac is great and all, but it's a jack of all trades and not a master of issue tracking. Below is the proposed feature list of DjTracker with their completion status. Everything marked as complete is 'done' at this time. This doesn't mean it won't change in the feature as new needs arise, but they're functional at this point.

*NOTE*
Extensive testing at this time has not been completed. In fact, a tests.py doesn't even exist yet. That'll come soon enough though.

------------------------
Project Creation:
------------------------

Every issue in DjTracker is attached to a corresponding Project. Each project is built of the following parts:

Components (complete):

Components are separate pieces of the overall beast that makes up a project. For instance, you may have a cart component in your ecommerce site.

Versions (complete):

Track multiple versions of your application by creating different version instance of your project. This way you can track issues against the latest version, while you also can continue to supporte users using legacy versions of your software.

Milestones (complete):

This is used to help you keep track of issues as you're working towards a major milestone in the product development. This'll allow you to view all issues still open before you reach the milestone completion point.

Permissions (95% complete):

DjTracker supports a permission scheme involving row level permissions. There are 3 levels of permissions:

	1. View:
		Allow users to simply view an issue. This is the base permission, and is required for most all other permissions. You can't edit what you can't see.

	2. Modify:
		Users with modification permissions can change the status of an issue, and otherwise adjust the issue anyway they see fit.

	3. Comment:
		This'll be the permission that you give to most users. This will give them the ability to create an issue, and comment on the issue. They will not be able to modify the issue though.

These permissions break down into three methods so that you can give groups, individual users, or anonymous

Git Repo Polling (complete):

DjTracker can polling a git repo's commits, and auto-update issues based on a certain string. This is pretty common in other issue trackers as well. You can set this up by setting the "Git Repo Path" of a project, which correlates to a location on your *filesystem*. gitpython doesn't handle parsing git URLs as far as I can tell yet, so you need to have the repo checked out on the server. This has a couple of drawbacks, such as you'll need to setup a cron to pull down commits to that repo on a semi-regular basis. 

You'll also need to initialize the project by giving it a starting commit hash as well. This allows the git poller to have a starting location in the git log to parse from. It'll then be able to parse from that commit forward. Again, some drawbacks, it'll brute force the list of commits, meaning that it can find commits in other branches than the master. Again, this appears to me as another limit of the 'gitpython' package. (Note: I don't mean any ill towards gitpython, I love the package, and I'm sure it'll continue its improvement.)

In the end of commit message is found containing "Fixes #ISSUE_NUMBER" (i.e. "Fixes #123") it'll auto-comment on the issue, and close it out.

SVN Repo Polling (complete):

SVN polling works pretty similar to Git polling. There's just a few minor difference, such as you can use a URL for the path, so you don't have to have a local checkout. Also, you can specify a username/password as well for these repos.

Repo Polling Cron Job Examples::

	*/5 * * * * /usr/bin/python /path/to/manage.py svn_poller

	*/5 * * * * /usr/bin/python /path/to/manage.py git_poller

One final note, if you're using SVN over SSH, you'll want to setup SSH keys in some fashion for your user. Otherwise SSH will prompt the cronjob for a password.

------------------------------------------------
Issue Creation (complete):
------------------------------------------------

Issues are attached to projects via foreign keys. You can comment on issues, change their status, and the like assuming you have proper permissions. You can also "watch" an issue if you're an authenticated user. This means that you'll receive email updates on any comments to an issue. In the future you'll get notified on status changes, and other modifications of the issue as well.

------------------------------------------------
User Profiles (80% complete):
------------------------------------------------

Currently I don't see an excessively large need for these, but that could change depending on use cases. As a result I went ahead and built a user profile module just in case. It's currently very limited, but you can view your profile (and the profile of others) to see what issues they have assigned to them. 

------------------------------------------------
Installation:
------------------------------------------------

Currently you can clone the github repository for your installation needs. Just clone it, and then run "python setup.py build; python setup install". This will install it to your python path. You can then enter the example app path that's included with your clone, and run the following "python manage.py syncdb; python manage runserver" to get up and running. If you wish to other plug the application into your setup you can do the following:

Dependencies:

django-registration
gitpython

Settings:

There's only two setting additions you'll need:

ISSUE_ADDRESS = "user@example.com"
WEB_SERVER = "apache"

This is the address issue updates will be sent from, and to handle sending files from protected locations. WEB_SERVER can be 'apache' or 'nginx'. The app will default to Apache if left unset. If you do use Apache you will need to install the mod_xsendfile module ( http://tn123.ath.cx/mod_xsendfile/ ). Using this you may run into the issue that /media/attachments/ will be served by Apache regardless, if they go directly to the path of the file where Apache will serve it. This can be circumvented with a directive such as::

	<Directory /var/www/domains/f4ntasmic.com/issues/htdocs/media/attachments/>
		Deny from all
	</Directory>

Django will still be able to get there, but everyday users won't be able to. This will lock it down so that only authenticated users can get to the file. Nginx, much more straight forward.

URLs:

You'll need the following URL pattern:

(r'', include('djtracker.urls')),

Feel free to change the path to suit your needs. Keep in mind it's only been tested at a root path thus far. It should work fine at other paths though.
                
