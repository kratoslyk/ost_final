from google.appengine.ext import db

class Category(db.Model):
  name = db.StringProperty(required=True)
  #creator = db.UserProperty(auto_current_user_add=True)

class Item(db.Model):
  name = db.StringProperty(required=True)
  count = db.IntegerProperty()
  ref = db.ReferenceProperty(Category,collection_name='items')
