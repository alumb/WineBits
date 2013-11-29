from models import Vintner, PostError
import regions

import os
import json

import webapp2
from google.appengine.ext import ndb

debug=os.environ["DEBUG"]

class SearchHandler(webapp2.RequestHandler):
    """
    /search
    """

    def get(self):
        pass

class VintnerBaseHandler(webapp2.RequestHandler):
    """
    GET /vintner : a search interface for vintners
    POST /vintner : create a vintner
    """

    def get(self):
        """
        /vintner?country=Canada
        /vintner?name=Bla
        """
        self.response.write("Search Interface Goes Here")

    def post(self):
        post = self.request.POST

        vintner = Vintner()
        try:
            key = vintner.create( post )
        except PostError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.response.content_type="text/plain"
        self.response.write(key)

class VintnerHandler(webapp2.RequestHandler):
    """
    /vintner/<id>
    """

    def get(self, vintner_id):
        vintner_key = ndb.Key(Vintner, int(vintner_id))

        vintner = vintner_key.get()
        response_obj = vintner.to_dict()
        response_obj['key'] = vintner_key.id()

        self.response.content_type="application/json"

        if debug:
            self.response.write( json.dumps(response_obj, indent=2 ))
        else:
            self.response.write( json.dumps(response_obj) )

class VintnerWineBaseHandler(webapp2.RequestHandler):
    def get(self, vintner_id):
        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()
        self.response.write("Wines for vintner")

    def post(self, vintner_id):
        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()

class VintnerWineHandler(webapp2.RequestHandler):
    def get(self, vintner_id, wine_id):
        pass


routes = [
            (r'/search', SearchHandler),
            (r'/vintner', VintnerBaseHandler),
            (r'/vintner/(\d+)', VintnerHandler),
            (r'/vintner/(\d+)/wine', VintnerWineBaseHandler),
            (r'/vintner/(\d+)/wine/(\d+)' VintnerWineHandler)
        ]
