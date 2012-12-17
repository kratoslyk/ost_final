import category
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import os

class ExportHandler(webapp.RequestHandler):
    def get(self):
      qstr=urllib.unquote_plus(self.request.query_string)
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]
      #self.response.out.write('&ltCATEGORY&gt&nbsp\n')
      #self.response.out.write('&ltNAME&gt{0}&lt/NAME&gt\n'.format(qstr))
      #self.response.out.write('&lt/CATEGORY&gt\n')
      items=[]
      if not cat is None:
        for val in cat.items:
          items.append(val.name)
          
      template_values = {'cname':qstr, 'items':items}
      path = os.path.join(os.path.dirname(__file__), 'exportTemplate.html')
      self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/export?[^/]+', ExportHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
