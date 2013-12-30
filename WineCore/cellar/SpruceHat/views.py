from cellar.SpruceHat.stubs import webapp2, ndb, debug, search
from google.appengine.api import users


import os
import json


def get_url(model):
    """
        >>> v = Winery()
        >>> key = v.create({'name':'Winery'})
        >>> get_url(v)
        '/winery/stub-key'

        >>> w = Wine(parent=key)
        >>> key = w.create({'winetype':'Red', 'year':'2010'}, v)
        >>> get_url(w)
        '/winery/stub-key/wine/stub-key'
    """
    print "this is a test"
    if isinstance(model, Winery):
        return "/winery/%s" % str(model.key.id())
    if isinstance(model, Wine):
        parent_key = model.key.parent()
        return "/winery/%s/wine/%s" % (str(parent_key.id()), str(model.key.id()))
    return None


class MyHandler(webapp2.RequestHandler):
    @staticmethod
    def json(model):
        """
        Converts Models into dicts
        >>> v = Winery()
        >>> key = v.create({'name':'Winery'})
        >>> MyHandler.json(v)
        {...'name': 'Winery'...}

        Adds Model links
        >>> MyHandler.json(v)
        {...'url': '/winery/stub-key'...}

        Flattens json elements
        >>> MyHandler.json({'json':{'thing':'awesome'}})
        {...'thing': 'awesome'...}
        """
        try:
            url = get_url(model)
            try:
                id_ = model.key.id()
            except:
                id_ = None
            if not isinstance(model, dict):
                object_ = model.to_dict()
            else:
                object_ = model
            if object_ and 'json' in object_ and object_['json']:
                for key, value in object_['json'].iteritems():
                    object_[key] = value
                del object_['json']
            if url:
                object_['url'] = url
            if id_:
                object_['id'] = id_
            return object_
        except AttributeError as e:
            return model

    def json_response(self, model):
        """
        Return object_ as JSON, with 'application/json' type.
        Strip out any 'json' field

        """
        if type(model) != list:
            object_ = MyHandler.json(model)
        else:
            object_ = [MyHandler.json(o) for o in model]

        self.response.content_type="application/json"
        if debug:
            self.response.write( json.dumps(object_, indent=2 ))
        else:
            self.response.write( json.dumps(object_) )


class bob():
    print "test"

class BaseHandler(MyHandler):
    """
    / : returns a 'hello' sort of deal. 
    """

    def get(self):
        user = users.get_current_user()

        self.response.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>WineBits: WineCellar</title>
    <link rel="stylesheet" href="/style/css/bootstrap.min.css" />
    <script src="/style/js/bootstrap.min.js"></script>
    <link href='http://fonts.googleapis.com/css?family=Roboto+Slab:400,100,700,300' rel='stylesheet' type='text/css'>
  </head>
  <body>
    <h1> Welcome to WineCellar.</h1>
    <p> hello: """ + user.nickname() + """</p>
    <p> Sign-out: <a href=\"""" + users.create_logout_url("") + """\">Logout</a> </p>
  </body>
</html>
                """)

routes = [
            (r'/', BaseHandler), 
        ]
