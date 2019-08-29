#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Abhishek Pednekar'
SITENAME = 'Code Disciples'
SITEURL = 'https://codedisciples.in'

## Development and testing
# SITEURL = "http://localhost:8000"
SITESUBTITLE = u'A blog for all things code'

PATH = 'content'

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

# Theme info - https://github.com/arulrajnet/attila
#THEME = "themes/attila"
THEME = "themes/voidy-bootstrap"

# Overriding CSS for the rss icon
# CSS_OVERRIDE = ['theme/css/blog.css']
# COLOR_SCHEME_CSS = 'monokai.css'

STYLESHEET_FILES = ("blog.css", "pygment.css")

SIDEBAR = "sidebar.html"

DEFAULT_PAGINATION = 5

FAVICON = "static/images/favicon.ico"

# Image for the home page
# HOME_COVER = "static/images/black-gradient-home.jpg"


# Post and Pages path
# ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
# ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
# PAGE_URL = 'pages/{slug}/'
# PAGE_SAVE_AS = 'pages/{slug}/index.html'
# YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
# MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# # Tags and Category path
# CATEGORY_URL = 'category/{slug}'
# CATEGORY_SAVE_AS = 'category/{slug}/index.html'
# CATEGORIES_SAVE_AS = 'catgegories.html'
# TAG_URL = 'tag/{slug}'
# TAG_SAVE_AS = 'tag/{slug}/index.html'
# TAGS_SAVE_AS = 'tags.html'

# # Author
# AUTHOR_URL = 'author/{slug}'
# AUTHOR_SAVE_AS = 'author/{slug}/index.html'
# AUTHORS_SAVE_AS = 'authors.html'

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