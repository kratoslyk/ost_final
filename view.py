import category
import pair
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.etree import ElementTree
import os
import random

def randFunc(l):
  b=random.randint(0,l)
  a=random.randint(0,l)
  while b==a:
    b=random.randint(0,l)
  return [a,b]

class ViewHandler(webapp.RequestHandler):
    def get(self):
      qstr=urllib.unquote_plus(self.request.query_string)
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]
      ps=[]
      if not cat is None:
        i=cat.items.count()
        if i<2 :
           self.redirect("/error?lessitem")
           return
        ints= randFunc(i-1)
        c=0
        for val in cat.items:
          if c in ints:
            p=pair.Pair(val.name,urllib.quote_plus(val.name))
            ps.append(p)
          c=c+1
      url=urllib.quote_plus(qstr)
      template_values = {'cname':qstr, 'ps':ps, 'url':url}
      path = os.path.join(os.path.dirname(__file__), 'viewTemplate.html')
      self.response.out.write(template.render(path, template_values))

class VoteHandler(webapp.RequestHandler):
    def get(self):
      qstr=urllib.unquote_plus(self.request.query_string)
      if not qstr:
          self.redirect('/error?noarg')
          return
      itms = db.GqlQuery("SELECT * FROM Item WHERE name= :1",qstr)
      if itms and itms.count() == 1:
        item = itms[0]
        item.count = item.count+1
        item.put()
      else:
         self.redirect('/error?noitem')
         return
      cat=itms[0].ref
      url=urllib.quote_plus(cat.name)
      self.redirect('/view?'+url)


application = webapp.WSGIApplication(
                                     [('/view?[^/]+', ViewHandler),
                                      ('/vote?[^/]+', VoteHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
