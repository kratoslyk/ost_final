import category
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import os

class CommentHandler(webapp.RequestHandler):
    def get(self):
      qstr=urllib.unquote_plus(self.request.query_string)
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]

      items=[]
      if not cat is None:
        for val in cat.items:
          items.append(val.name)
      url=urllib.quote_plus(qstr)
      template_values = {'cname':qstr, 'items':items,'url':url}
      path = os.path.join(os.path.dirname(__file__), 'commentTemplate.html')
      self.response.out.write(template.render(path, template_values))

    def post(self):
      user=users.get_current_user()
      qstr=urllib.unquote_plus(self.request.query_string)
      url=urllib.quote_plus(qstr)
      choice = self.request.get('choice')
      comts = self.request.get('comments')
      if not choice or not comts:
        self.redirect('/error?noarg')
        return
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]
      item= None
      for var in cat.items:
         if choice==var.name:
            item=var
            for c in item.comments:
              if c.writer==user:
                 self.redirect('/error?hascomment')
                 return
            com=category.Comment()
            com.text=comts
            com.ref=item
            com.put()
            self.redirect('/result?'+url)
            return
      self.redirect('/error?noitem')
      

application = webapp.WSGIApplication(
                                     [('/comment?[^/]+', CommentHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
