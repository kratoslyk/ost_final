import category
import urllib
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.etree import ElementTree
import os
import pair

class ResultHandler(webapp.RequestHandler):
    def get(self):
      qstr=urllib.unquote_plus(self.request.query_string)
      cats = db.GqlQuery("SELECT * FROM Category WHERE name= :1",qstr)
      cat = None
      if cats and cats.count() == 1:
         cat = cats[0]
      ps=[]
      url=urllib.quote_plus(qstr)
      if not cat is None:
        for val in cat.items:
          ss="{0} : {1}".format(val.name,val.count)
          cmts=""
          for cm in val.comments:
              cmts += "&nbsp&nbsp&nbsp-- {0} says: {1}</br>".format(cm.writer,cm.text)
          p=pair.Pair(ss,cmts)
          ps.append(p)
          
      template_values = {'cname':qstr, 'ps':ps, 'url':url}
      path = os.path.join(os.path.dirname(__file__), 'resultTemplate.html')
      self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/result?[^/]+', ResultHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
