import category
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext import blobstore
from xml.etree import ElementTree
import os

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
      if rs.count > 0:
          self.redirect('/error?catexist')
          return
      cat=category.Category(name=cname)  
      cat.put()
      url=urllib.quote_plus(cname)
      self.redirect('/add?'+url)

class AddHandler(webapp.RequestHandler):
    def get(self,str):
      qstr=urllib.unquote_plus(self.request.query_string)
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]
      its=[]
      if not cat is None:
        for val in cat.items:
          its.append(val.name)
      url=urllib.quote_plus(qstr)
      template_values = {'cname':qstr, 'items':its, 'url':url}
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
        item = category.Item(name=iname,count=0,ref=cats[0])
        item.put()
      url=urllib.quote_plus(qstr)
      self.redirect('/add?'+url)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    file_contents = self.get_uploads('catfile')
    #print file_contents
    #print 'HI...'
    root = ElementTree.fromstring(file_contents[0])
    cate=Category()
    cate.name=root[0].text
    i=0;
    for child in root:
      if child.tag== 'ITEM':
        cate.items[i]=child[0].text
        i=i+1
    cate.put()
    self.redirect('/createCat')


application = webapp.WSGIApplication(
                                     [('/add?([^/]+)', AddHandler),
                                      ('/createCat', CreationHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
