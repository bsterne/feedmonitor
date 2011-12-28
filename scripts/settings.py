# configuration options for feed monitor

# list of RSS feeds to scan
FEEDS = ['http://feed1.example.com/feed.rss',
         'http://feed2.example.net/feed.rss'
         ]

# strings to look for in the feeds
# for a pattern to match, all words in each list must be present
# in the search string
PATTERNS = [['term1', 'term2'],
            ['term3'],
            ['term4', 'term5', 'term6']
            ]

# Database settings
DB_HOST = ""
DB_USER = ""
DB_PASS = ""
DB_NAME = ""

# Email settings
# address to send from
EMAIL_FROM = "sender@example.org"
# list of addresses to send the report to
EMAIL_TO   = ['person1@example.com', 'person2@example.net']
SMTP_HOST = "smtp.example.org"
SMTP_PORT = 465 # change this if you don't want SSL

# LDAP settings
LDAP_USER = ""
LDAP_PASS = ""
