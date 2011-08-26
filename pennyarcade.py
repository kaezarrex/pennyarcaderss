#!/usr/bin/env python

from urllib2 import urlopen, URLError
from xml.etree import ElementTree as etree
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class PennyArcadeHandler(webapp.RequestHandler):

    HTML_LINK_MATCH = re.compile('<link>\s*.+/comic/(\d+)/(\d+)/(\d+)/?\s*</link>')
    HTML_DESCRIPTION_MATCH = re.compile('<description>\s*<!\[CDATA\[\s*(New Comic.+)\s*]]>\s*</description>')

    def get(self):
    
        try:
            page = urlopen('http://penny-arcade.com/feed').read()
        except URLError, e:
            return
        
        links = re.findall(PennyArcadeHandler.HTML_LINK_MATCH, page)
        descriptions = re.findall(PennyArcadeHandler.HTML_DESCRIPTION_MATCH, page)

        for i in range(len(links)):
            page = page.replace(descriptions[i], descriptions[i] + '<img src="http://pennyarcaderss.appspot.com/comic/' + '/'.join(links[i]) + '/">')


        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(page)


class ComicHandler(webapp.RequestHandler):

    HTML_COMIC_MATCH = re.compile('"post comic">\s*<img src="(.+\.jpg)"')

    def get(self, year, month, day):

        try:
            page = urlopen('http://penny-arcade.com/comic/' + '/'.join([year, month, day])).read()
        except URLError, e:
            return

        comic = re.findall(ComicHandler.HTML_COMIC_MATCH, page)[0]

        self.redirect(comic, permanent=True)

        return

def main():
    application = webapp.WSGIApplication([('/?', PennyArcadeHandler), ('/comic/(\d+)/(\d+)/(\d+)/?', ComicHandler)], debug=False)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
