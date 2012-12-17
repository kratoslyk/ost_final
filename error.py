
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.etree import ElementTree
import os

class ErrorHandler(webapp.RequestHandler):
    def get(self,str):
        qstr=self.request.query_string
        msg='No Error'
        if qstr=='catexist':
           msg='Error: Creating an existing category.'
        elif qstr=='noarg':
           msg='Error: Passing empty arguments to server.'
        elif qstr=='sameitem':
           msg='Error: Item exists.'
        elif qstr=='noitem':
           msg='Error: Item not found.'
        elif qstr=='notowner':
           msg='Error: You are not the owner.'
        elif qstr=='hascomment':
           msg='Error: You already have a comment on this item.'
        template_values = {'msg':msg}
        path = os.path.join(os.path.dirname(__file__), 'errorpage.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/error?([^/]+)', ErrorHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
