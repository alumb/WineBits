from models import Vintner, YouNeedATokenForThat
import regions

import os
import json

from stubs import webapp2, ndb, debug


class MyHandler(webapp2.RequestHandler):
    def json_response(self, object_):
        """
        Return object_ as JSON, with 'application/json' type.
        Strip out any 'json' field
        """
        if 'json' in object_:
            for key, value in object_['json']:
                object_[key] = value
            del object_['json']

        self.response.content_type="application/json"
        if debug:
            self.response.write( json.dumps(object_, indent=2 ))
        else:
            self.response.write( json.dumps(object_) )


class SearchHandler(webapp2.RequestHandler):
    """
    /search
    """

    def get(self):
        pass


class VintnerBaseHandler(MyHandler):
    """
    GET /vintner : fetch a set of vintners
    POST /vintner : create a vintner
    """

    def get(self):
        """
        /vintner?country="Canada"
        /vintner?name="Black Hills Estate"
        """
        self.response.write("Vintner List Interface Goes Here")

    def post(self):
        """

        >>> v = VintnerBaseHandler()
        >>> v.request.POST = {'name':'Winery'}
        >>> v.post()
        >>> v.response.content_type
        'text/plain'
        >>> v.response.last_write
        'stub-key'

        """
        post = self.request.POST

        vintner = Vintner()
        try:
            key = vintner.create( post )
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.response.content_type="text/plain"
        self.response.write(key)


class VintnerHandler(MyHandler):
    """
    /vintner/<id>
    """

    def get(self, vintner_id):
        """
        >>> v = Vintner()
        >>> key = v.create({'name':'winery'})
        >>> ndb.Key.load_get(v )

        >>> h = VintnerHandler()
        >>> h.get('12345')
        >>> h.response.content_type
        'application/json'
        >>> h.response.last_write
        '{..."name": "winery",..."key":...}'
        """

        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()
        if not vintner:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        response_obj = vintner.to_dict()
        response_obj['key'] = vintner_key.id()

        self.json_response(response_obj)

    def post(self, vintner_id):
        """
        >>> v = Vintner()
        >>> key = v.create({'name':'winery'})
        >>> ndb.Key.load_get(v )

        >>> h = VintnerHandler()
        >>> h.request.POST = {'location':'Canada'}
        >>> h.post('12345')
        >>> h.response.content_type
        'application/json'
        >>> h.response.last_write
        '{..."country": "Canada"..."name": "winery",..."key":...}'
        """

        post = self.request.POST

        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()

        try:
            vintner.update(post)
        except YouNeedATokenForThat as e:
            self.response.write(str(e))
            self.response.status = "401 Unauthorized"
            return

        response_obj = vintner.to_dict()
        response_obj['key'] = vintner_key.id()

        self.json_response(response_obj)


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
            (r'/vintner/(\d+)/wine/(\d+)', VintnerWineHandler)
        ]
