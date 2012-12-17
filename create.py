import category
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from xml.etree import ElementTree
import os
import pair


class CreationHandler(webapp.RequestHandler):
    def get(self):
      template_values = {}
      path = os.path.join(os.path.dirname(__file__), 'createTemplate.html')
      self.response.out.write(template.render(path, template_values))
    def post(self):
      cname=self.request.get('catname')
      if not cname:
         self.redirect('/error?noarg')
         return
      rs = db.GqlQuery("SELECT * FROM Category WHERE name= :1",cname)
      if rs.count() > 0:
          self.redirect('/error?catexist')
          return
      cat=category.Category(name=cname)  
      cat.put()
      url=urllib.quote_plus(cname)
      self.redirect('/add?'+url)

class AddHandler(webapp.RequestHandler):
    def get(self,str):
      user = users.get_current_user()
      qstr=urllib.unquote_plus(self.request.query_string)
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]
      ps=[]
      if not cat is None:
        if user != cat.creator:
          self.redirect("/error?notowner")
          return
        for val in cat.items:
          p=pair.Pair(val.name,urllib.quote_plus(val.name))
          ps.append(p)
      url=urllib.quote_plus(qstr)
      template_values = {'cname':qstr, 'pairs':ps, 'url':url}
      path = os.path.join(os.path.dirname(__file__), 'addTemplate.html')
      self.response.out.write(template.render(path, template_values))
    def post(self,str):
      qstr=urllib.unquote_plus(self.request.query_string)
      iname=self.request.get('item')
      if not iname:
          self.redirect('/error?noarg')
          return
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      if cats and cats.count() == 1:
        for var in cats[0].items:
            if var.name == iname:
               self.redirect('/error?sameitem')
               return
        item = category.Item(name=iname,count=0,ref=cats[0])
        item.put()
      url=urllib.quote_plus(qstr)
      self.redirect('/add?'+url)

class UploadHandler(webapp.RequestHandler):
  def post(self):
    file_content = self.request.get('catfile')
    if not file_content:
       self.redirect('/error?noarg')
       return
    root = ElementTree.fromstring(file_content)
    cate=category.Category(name=root[0].text)
    rs = db.GqlQuery("SELECT * FROM Category WHERE name= :1",cate.name)
    if rs.count() > 0:
       #for c in root:
        #  if c.tag== 'ITEM':
         #    for item in rs[o].items:
                
       self.redirect('/error?catexist')
       return
    cate.put()
    for child in root:
      if child.tag== 'ITEM':
        itm=category.Item(name=child[0].text)
        itm.count=0
        itm.ref=cate
        itm.put()
    
    self.redirect('/')


application = webapp.WSGIApplication(
                                     [('/add?([^/]+)', AddHandler),
                                      ('/createCat', CreationHandler),
                                      ('/import',UploadHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
