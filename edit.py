import category
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import os

class EditHandler(webapp.RequestHandler):
    def post(self):
      qstr=urllib.unquote_plus(self.request.query_string)
      itemold=self.request.get('itemold')
      itemnew=self.request.get('itemnew')
      if not itemold or not itemnew:
         self.redirect('/error?noarg')
         return
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]

      if not cat is None:
        for val in cat.items:
          if val.name==itemnew:
            self.redirect('/error?sameitem')
            return

      if not cat is None:
        for val in cat.items:
          if val.name==itemold:
             val.name=itemnew
             val.count=0
             val.put()
             url=urllib.quote_plus(qstr)
             self.redirect('/add?'+url)
             return
      self.redirect('/error?noitem')

application = webapp.WSGIApplication(
                                     [('/edit?[^/]+', EditHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
