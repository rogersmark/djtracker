Email Handling
*****************************

DjTracker has the ability to parse email addresses for new comments and new issues. Currently this only supports IMAP, but POP3 support is planned for the future. 

Email Settings
=============================

The following settings are required in your settings.py in order to leverage the usage of email parsing:

* ISSUE_PARSE_EMAIL - This needs to be True in order for email parsing to occur.
* ISSUE_MAIL_SSL - If you use SSL, this needs to be True. Otherwise non-ssl will be used
* ISSUE_MAIL_HOST - This will be the name of your IMAP server, i.e. imap.gmail.com
* ISSUE_MAIL_USER - This will be used for authentication to your mail server
* ISSUE_MAIL_PASSWORD - This will be used for authentication to your mail server

Expected Email Subjects
=============================

DjTracker needs email subjects to be formed in a certain fashion in order to properly create issues on your behalf. If you're creating a new issue via email, the following subject is expected:

    DjTracker: [project-slug]: Your Title
    
If you're responding on an issue, you'd use the following:

    DjTracker: [project-slug]: Issue #5
    
That'll add the comment onto the end of the current issue with an ID of 5. 
