#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Abhishek Pednekar'
SITENAME = 'Code Disciples'
# SITEURL = 'https://codedisciples.in'

# Development and testing. Uncomment when running on local server and comment out the production URL
SITEURL = "http://localhost:8000"

SITESUBTITLE = u'A blog for all things code'

PATH = 'content'

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

# Theme info - https://github.com/robulouski/voidy-bootstrap
THEME = "themes/voidy-bootstrap"

STYLESHEET_FILES = ("blog.css", "tomorrow_night.css")

SIDEBAR = "sidebar.html"

DEFAULT_PAGINATION = 5

FAVICON = "static/images/logo.png"

# Author bio
AUTHORS_BIO = {
    "abhishek pednekar": {
        "name": "Abhishek Pednekar",
        "cover": "static/images/black-gradient-author.jpg",
        "image": "",
        "website": "http://codedisciples.in",
        "linkedin": "unavailable",
        "github": "AbhishekPednekar84",
        "location": "Bangalore",
        "bio": "Get in touch :)"
    }
}

# Path to the rss xml
RSS = 'feeds/all.atom.xml'

# Comments - https://disqus.com/home/forums/codedisciples/
DISQUS_SITENAME = "code-disciples"

# Analytics
GOOGLE_ANALYTICS = "UA-145611420-1"

# Google site verification
GOOGLE_SITE_VERIFICATION = "PUuuDE6varF3pT3Vgy0WO0YJqvRxjfwVqwxo9Jz1awE"

# Add tags to the sidebar
CUSTOM_SIDEBAR_MIDDLES = ("sb_taglist.html", )
