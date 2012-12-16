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

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, ' + user.nickname())
        else:
            #self.redirect(users.create_login_url(self.request.uri))
            #self.redirect('/voting')
            cats = db.GqlQuery("SELECT * FROM Category")

            ps=[]
            for var in cats:
               p=pair.Pair(var.name,urllib.quote_plus(var.name))
               ps.append(p)
            template_values = {
            'pname': 'Voting System',
            'cats': ps
            }
            path = os.path.join(os.path.dirname(__file__), 'main.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
