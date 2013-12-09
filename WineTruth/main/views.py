from models import Winery, Wine, YouNeedATokenForThat
import regions
import wine_types

import os
import json

from stubs import webapp2, ndb, debug

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


class LocationHandler(MyHandler):
    """
    GET /location : an exhaustive list of every location
    GET /location?fuzzy=true : every location_fuzzy
    """
    #TODO: test LocationHandler
    def get(self):
        if 'fuzzy' in self.request.GET:
            response = [{'location_fuzzy':location}
                        for location in Winery.all_fuzzy_locations()]
            self.json_response(response)
        else:
            response = [{'location':location}
                        for location in regions.location_list]
            self.json_response(response)

class VarietalHandler(MyHandler):
    """
    /varietal : all varietals
    """
    #TODO: test VarietalHandler
    #TODO: create fuzzy Varietal
    def get(self):
        response = [{'varietal':varietal}
                    for varietal in wine_types.wine_options]
        self.json_response(response)

class WineTypeHandler(MyHandler):
    """
    /winetype : all wine-types
    """
    #TODO: test WineTypeHandler
    def get(self):
        response = [{'winetype':winetype}
                    for winetype in wine_types.types]
        self.json_response(response)

class CountryHandler(MyHandler):
    """
    GET /country : list countries
    """
    #TODO: test CountryHandler

    def get(self):
        response = [{'country':country} for country in regions.countries]
        self.json_response(response)

class RegionHandler(MyHandler):
    """
    GET /country/Canada : list regions
    """
    #TODO: test RegionHandler

    def get(self, country):
        response = [{'region':region,'country':country}
                    for region in regions.regions_for_country(country)]
        self.json_response(response)

class SubRegionHandler(MyHandler):
    """
    GET /country/Canada/British Columbia : list subregions
    """
    #TODO: test SubRegionHandler

    def get(self, country):
        response = [{'subregion': subregion}
                     for subregion in regions.subregions_for_country(country, region)]
        self.json_response(response)

class WineryBaseHandler(MyHandler):
    """
    GET /winery : fetch a set of winerys
    POST /winery : create a winery
    """

    def get(self):
        """
        /winery?country=Canada
        /winery?region=British Columbia
        /winery?subregion=Okanagan Valley
        /winery?name="Black Hills Estate"
        /winery?location="Canada - British Columbia: Okanagan Valley"
        /winery?location_fuzzy="Somewhere"
        """
        #TODO: Compound Queries
        #TODO: convert location query into country/region/subregion query
        get = self.request.GET
        if 'subregion' in get:
            self.json_response(Winery.subregion_query(get['subregion']))
            return
        if 'region' in get:
            self.json_response(Winery.region_query(get['region']))
            return
        if 'country' in get:
            self.json_response(Winery.country_query(get['country']))
            return
        if 'name' in get:
            self.json_response(Winery.name_query(get['name']))
            return
        if 'location' in get:
            self.json_response(Winery.location_query(get['location']))
            return
        if 'location_fuzzy' in get:
            self.json_response(Winery.location_fuzzy_query(
                               get['location_fuzzy']))
            return
        if 'verified_by' in get:
            self.json_response(Winery.verified_by_query(
                               get['verified_by']))
            return
        if 'verified' in get:
            verified = False
            if get['verified'].lower() == 'true':
                verified = True
            self.json_response(Winery.verified_query(verified))
            return
        self.response.write("Winery List Interface Goes Here")

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
            key = winery.create( post )
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.json_response(winery)


class WineryHandler(MyHandler):
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

        self.json_response(winery)

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
            winery.update(post)
        except YouNeedATokenForThat as e:
            self.response.write(str(e))
            self.response.status = "401 Unauthorized"
            return

        self.json_response(winery)


class WineryWineBaseHandler(MyHandler):
    def get(self, winery_id):
        """
        /winery/12345/wine => all wines for winery
        """
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        if not winery:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        self.json_response(winery.wine_query())

    def post(self, winery_id):
        """
        POST /winery/12345/wine => create a wine for winery
        """
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        if not winery:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        post = self.request.POST

        wine = Wine(parent=winery_key)
        try:
            key = wine.create( post, winery )
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.json_response(wine)

class WineryWineHandler(MyHandler):
    def get(self, winery_id, wine_id):
        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        self.json_response(wine)

    def post(self, winery_id, wine_id):
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()
        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not winery or not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        post = self.request.POST

        try:
            wine.update(post, winery)
        except YouNeedATokenForThat as e:
            self.response.write(str(e))
            self.response.status = "401 Unauthorized"
            return

        self.json_response(wine)



class SearchHandler(MyHandler):
    """
    /search
    """

    def get(self):
        pass


routes = [
            (r'/location', LocationHandler),
            (r'/winetype', WineTypeHandler),
            (r'/varietal', VarietalHandler),
            (r'/country', CountryHandler),
            (r'/country/([\w\s\d%]+)', RegionHandler),
            (r'/country/([\w\s\d%]+)/([\w\s\d%]+)', SubRegionHandler),
            (r'/winery', WineryBaseHandler),
            (r'/winery/(\d+)', WineryHandler),
            (r'/winery/(\d+)/wine', WineryWineBaseHandler),
            (r'/winery/(\d+)/wine/(\d+)', WineryWineHandler),
            (r'/search', SearchHandler),
        ]
