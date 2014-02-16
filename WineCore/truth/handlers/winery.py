from truth.models.base import YouNeedATokenForThat
from truth.stubs import webapp2, ndb
from truth.views.jsonview import json_response
from truth.models.wine import Wine
from truth.models.winery import Winery
from truth.models.event import Event


class WineryBaseHandler(webapp2.RequestHandler):
    """
    GET /winery : fetch a set of winerys
    POST /winery : create a winery
    """

    def get(self):
        """
        /winery?
        /winery?country=Canada
        /winery?region=British Columbia
        /winery?subregion=Okanagan Valley
        /winery?name="Black Hills Estate"
        /winery?location="Canada - British Columbia: Okanagan Valley"
        /winery?location_fuzzy="Somewhere"
        """
        get = self.request.GET
        if 'subregion' in get:
            json_response(self, Winery.subregion_query(get['subregion']))
            return
        if 'region' in get:
            json_response(self, Winery.region_query(get['region']))
            return
        if 'country' in get:
            json_response(self, Winery.country_query(get['country']))
            return
        if 'name' in get:
            json_response(self, Winery.name_query(get['name']))
            return
        if 'location' in get:
            json_response(self, Winery.location_query(get['location']))
            return
        if 'location_fuzzy' in get:
            json_response(self, Winery.location_fuzzy_query(
                          get['location_fuzzy']))
            return
        if 'verified_by' in get:
            json_response(self, Winery.verified_by_query(
                          get['verified_by']))
            return
        if 'verified' in get:
            verified = False
            if get['verified'].lower() == 'true':
                verified = True
            json_response(self, Winery.verified_query(verified))
            return

        #if no params, return entire list.
        json_response(self, Winery.all_query())

    def post(self):
        """

        >>> v = WineryBaseHandler()
        >>> v.request.POST = {'name':'Winery'}
        >>> v.post()
        >>> v.response.content_type
        'application/json'
        >>> v.response.last_write
        '{..."key": "stub-key"...}'

        """
        post = self.request.POST

        winery = Winery()
        try:
            key = winery.create(post)
            winery.update()
            Event.create(self.request.remote_addr, "Winery", key)
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        json_response(self, winery)


class WineryHandler(webapp2.RequestHandler):
    """
    /winery/<id>
    """

    def get(self, winery_id):
        """
        >>> v = Winery()
        >>> key = v.create({'name':'winery'})
        >>> ndb.Key.load_get(v )

        >>> h = WineryHandler()
        >>> h.get('12345')
        >>> h.response.content_type
        'application/json'
        >>> h.response.last_write
        '{..."name": "winery",..."key":...}'
        """

        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()
        if not winery:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        json_response(self, winery)

    def post(self, winery_id):
        """
        >>> v = Winery()
        >>> key = v.create({'name':'winery'})
        >>> ndb.Key.load_get(v )

        >>> h = WineryHandler()
        >>> h.request.POST = {'location':'Canada'}
        >>> h.post('12345')
        >>> h.response.content_type
        'application/json'
        >>> h.response.last_write
        '{..."country": "Canada"...}'
        >>> h.response.last_write
        '{..."name": "winery"...}'
        >>> h.response.last_write
        '{..."key":...}'
        """

        post = self.request.POST

        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        try:
            winery.modify(post)
            wines = Wine.winery_query(winery)
            winery.update(wines)
            Event.update(self.request.remote_addr, "Winery", winery_key)
        except YouNeedATokenForThat as e:
            self.response.write(str(e))
            self.response.status = "401 Unauthorized"
            return

        json_response(self, winery)

routes = [
    (r'/winery/?', WineryBaseHandler),
    (r'/winery/(\d+)/?', WineryHandler),
]
