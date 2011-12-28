#!/usr/bin/python
# Scan a list of RSS feeds for specific terms and send notification
# emails when terms are found
import urllib, string, sys, os, smtplib, time, MySQLdb, socket, re
from xml.dom import minidom
from settings import *

# print debugging output and do NOT make changes to the DB
if "--debug" in sys.argv:
    DEBUG = True
else:
    DEBUG = False

# set up urlopener to specify Firefox as the user-agent
# (some news feeds don't like the Python default user agent)
class AppURLopener(urllib.FancyURLopener):
    version = "User-Agent:Mozilla/5.0 (X11; Linux i686; rv:11.0a1) Gecko/20111220 Firefox/11.0a1"
urllib._urlopener = AppURLopener()

# set up database connection
try:
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
    c = db.cursor()
except:
    print "feedMonitor.py: can't connect to database\n"
    sys.exit()

# see if our filter matches a pattern, and if the record doesn't already exist
# in the DB
def filter(phrase, link):
    p = re.compile("[ \.,]")
    for pattern in PATTERNS:
        alert = True
        postWords = p.split(string.lower(phrase))
        for word in pattern:
            if word not in postWords:
                alert = False
        if alert:
            myQuery = "SELETC * FROM alerts WHERE link='%s';" % link
            if(c.execute(myQuery) == 0L):
                if DEBUG:
                    print "New Link Found:", link
                return True
    return False

# strip any single or double quotes
def stripQuotes(s):
    s = s.replace("\"","")
    s = s.replace("\'","")
    return s

# container for the items to monitor
posts = []

# container for items to alert on
alerts = []

# set socket timeout to 10 seconds so we're not waiting on feeds that are
# down or unresponsive
socket.setdefaulttimeout(10)

for f in FEEDS:
    try:
        u = urllib.urlopen(f)
        rssText = u.read()
        if DEBUG:
            print "Fetching %s:\nResponse headers:" % f
            print u.headers.items()
        # remove non-ASCII chars that can confuse the XML parser
        p = "[^\001-\176]"
        rssText = re.sub(p, "", rssText)
        try:
            xmldoc = minidom.parseString(rssText)
        except:
            print "feedMonitor - unable to read feed: %s" % f
            continue

        items = xmldoc.getElementsByTagName("item")
        for i in items:
            myTitle = i.getElementsByTagName("title")
            # special case for google feeds
            if "news.google.com" in f:
                temp = i.getElementsByTagName("link")[0].firstChild.toxml()
                temp = string.split(temp,"url=")[1]
                myLink = string.split(temp,"&amp;cid")[0]
            # everyone else doesn't require parsing the link out of the RSS item title - grr
            else:
                myLink = i.getElementsByTagName("link")[0].firstChild.toxml()
            # each post is a tuple containing the source, link, title, description of the vuln
            try:
                posts.append((f, myLink, myTitle[0].firstChild.toxml()))
            except: pass
    # catch exceptions for socket timeouts, etc.
    except:
        print "Exception for feed %s" % f
        print sys.exc_info()

# send each post to the keyword filter
# any posts that match on one or more filters will be added to the list of alerts
# to be mailed
for post in posts:
    if filter(post[2],post[1]):
        alerts.append(post)

# if there are any alerts found, mail them out
if len(alerts):
    headers = "From: %s\r\nTo: %s\r\n" % (EMAIL_FROM, ", ".join(EMAIL_TO))
    headers += "MIME-Version: 1.0\r\nContent-Type: text/html; charset=iso-8859-1\r\n"
    headers += "Subject: New Security %s Found - \"%s\"\r\n\r\n" % \
        ("Alert" if len(alerts) == 1 else "Alerts",
         alerts[0][2] if len(alerts) == 1 else alerts[0][2] + ", etc.")

    text = "<html><body><br>\n"
    for alert in alerts:
        text += alert[2] + " - <a href=\"" + alert[1] + "\">" + alert[1] + "</a><br><br>\n"
        myQuery = "INSERT INTO alerts(subject,link,source,date_sent) values('%s','%s','%s','%s');" % \
            (stripQuotes(alert[2]), stripQuotes(alert[1]), stripQuotes(alert[0]),
             time.strftime('%Y-%m-%d %H:%M:%S'))
        # show the query we _would_ use to log the alert
        if DEBUG:
            print myQuery
        # log the alert in the database
        else:
            c.execute(myQuery)
    # close out the HTML mail document and combine the headers and body
    text += "</body></html>"
    msg = headers + text

    # print only to the console
    if DEBUG:
        print msg
    else:
        # send out the mail
        s = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        s.login(LDAP_USER, LDAP_PASS)
        s.sendmail(EMAIL_FROM, EMAIL_TO, msg)
