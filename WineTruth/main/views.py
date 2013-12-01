from models import Vintner, Wine, YouNeedATokenForThat
import regions
import wine_types

import os
import json

from stubs import webapp2, ndb, debug

def get_url(model):
    """
        >>> v = Vintner()
        >>> key = v.create({'name':'Winery'})
        >>> get_url(v)
        '/vintner/stub-key'

        >>> w = Wine(parent=key)
        >>> key = w.create({'winetype':'Red', 'year':'2010'}, v)
        >>> get_url(w)
        '/vintner/stub-key/wine/stub-key'
    """
    if isinstance(model, Vintner):
        return "/vintner/%s" % str(model.key.id())
    if isinstance(model, Wine):
        parent_key = model.key.parent()
        return "/vintner/%s/wine/%s" % (str(parent_key.id()), str(model.key.id()))
    return None


def add_links(dict_):
    """
        Adds a key with the location's URL to the dict
        >>> add_links({'location':'blerg' })
        {...'vintner_location': '/vintner?location=blerg'...}

        Doesn't remove the original fields from the dict
        >>> add_links({'location':'blerg' })
        {...'location': 'blerg'...}

        >>> add_links({'location_fuzzy':'blerg'})
        {...'vintner_location_fuzzy': '/vintner?location_fuzzy=blerg'...}

        >>> add_links({'country':'Canada'})
        {...'vintner_country': '/vintner?country=Canada'...}

        >>> add_links({'country':'Canada', 'region':'British Columbia'})
        {...'vintner_region': '/vintner?region=British Columbia'...}

        >>> add_links({'country':'Canada', 'region':'British Columbia'})
        {...'region_subregions': '/country/Canada/British Columbia'...}

        >>> add_links({'subregion':'Okanagan'})
        {...'vintner_subregion': '/vintner?subregion=Okanagan'...}

    """
    if 'location' in dict_ and dict_['location']:
        location = dict_['location']
        dict_['vintner_location'] = "/vintner?location=%s" % location
    if 'location_fuzzy' in dict_ and dict_['location_fuzzy']:
        location = dict_['location_fuzzy']
        dict_['vintner_location_fuzzy'] = "/vintner?location_fuzzy=%s" % location
    if 'country' in dict_ and dict_['country']:
        country = dict_['country']
        dict_['vintner_country'] = "/vintner?country=%s" % country
        dict_['country_regions'] = "/country/%s" % country
    if 'region' in dict_ and 'country' in dict_ and dict_['region']:
        region = dict_['region']
        country = dict_['country']
        dict_['vintner_region'] = "/vintner?region=%s" % region
        dict_['region_subregions'] = "/country/%s/%s" % (country, region)
    if 'subregion' in dict_ and dict_['subregion']:
        subregion = dict_['subregion']
        dict_['vintner_subregion'] = "/vintner?subregion=%s" % subregion
    return dict_


class MyHandler(webapp2.RequestHandler):
    @staticmethod
    def json(model):
        """
        Converts Models into dicts
        >>> v = Vintner()
        >>> key = v.create({'name':'Winery'})
        >>> MyHandler.json(v)
        {...'name': 'Winery'...}

        Adds Model links
        >>> MyHandler.json(v)
        {...'url': '/vintner/stub-key'...}

        Flattens json elements
        >>> MyHandler.json({'json':{'thing':'awesome'}})
        {...'thing': 'awesome'...}

        Adds dict links
        >>> MyHandler.json({'country':'Canada'})
        {...'vintner_country': '/vintner?country=Canada'...}
        >>> MyHandler.json({'country':'Canada'})
        {...'country_regions': '/country/Canada'...}
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
            object_ = add_links(object_)
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
    #TODO: fold LocationHandler, WineTypeHandler, et-al into a megahandler
    def get(self):
        if 'fuzzy' in self.request.GET:
            response = [{'location_fuzzy':location}
                        for location in Vintner.all_fuzzy_locations()]
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

class VintnerBaseHandler(MyHandler):
    """
    GET /vintner : fetch a set of vintners
    POST /vintner : create a vintner
    """

    def get(self):
        """
        /vintner?country=Canada
        /vintner?region=British Columbia
        /vintner?subregion=Okanagan Valley
        /vintner?name="Black Hills Estate"
        /vintner?location="Canada - British Columbia: Okanagan Valley"
        /vintner?location_fuzzy="Somewhere"
        """
        #TODO: Compound Queries
        #TODO: convert location query into country/region/subregion query
        get = self.request.GET
        if 'subregion' in get:
            self.json_response(Vintner.subregion_query(get['subregion']))
            return
        if 'region' in get:
            self.json_response(Vintner.region_query(get['region']))
            return
        if 'country' in get:
            self.json_response(Vintner.country_query(get['country']))
            return
        if 'name' in get:
            self.json_response(Vintner.name_query(get['name']))
            return
        if 'location' in get:
            self.json_response(Vintner.location_query(get['location']))
            return
        if 'location_fuzzy' in get:
            self.json_response(Vintner.location_fuzzy_query(
                               get['location_fuzzy']))
            return
        if 'verified_by' in get:
            self.json_response(Vintner.verified_by_query(
                               get['verified_by']))
            return
        if 'verified' in get:
            verified = False
            if get['verified'].lower() == 'true':
                verified = True
            self.json_response(Vintner.verified_query(verified))
            return
        self.response.write("Vintner List Interface Goes Here")

    def post(self):
        """

        >>> v = VintnerBaseHandler()
        >>> v.request.POST = {'name':'Winery'}
        >>> v.post()
        >>> v.response.content_type
        'application/json'
        >>> v.response.last_write
        '{..."key": "stub-key"...}'

        """
        post = self.request.POST

        vintner = Vintner()
        try:
            key = vintner.create( post )
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.json_response(vintner)


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

        self.json_response(vintner)

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
        '{..."country": "Canada"...}'
        >>> h.response.last_write
        '{..."name": "winery"...}'
        >>> h.response.last_write
        '{..."key":...}'
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

        self.json_response(vintner)


class VintnerWineBaseHandler(MyHandler):
    def get(self, vintner_id):
        """
        /vintner/12345/wine => all wines for vintner
        """
        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()

        if not vintner:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        self.json_response(vintner.wine_query())

    def post(self, vintner_id):
        """
        POST /vintner/12345/wine => create a wine for vintner
        """
        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()

        if not vintner:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        post = self.request.POST

        wine = Wine(parent=vintner_key)
        try:
            key = wine.create( post, vintner )
            vintner.update_rank()
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.json_response(wine)

class VintnerWineHandler(MyHandler):
    def get(self, vintner_id, wine_id):
        wine_key = ndb.Key(Vintner, int(vintner_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        self.json_response(wine)

    def post(self, vintner_id, wine_id):
        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()
        wine_key = ndb.Key(Vintner, int(vintner_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not vintner or not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        post = self.request.POST

        try:
            wine.update(post, vintner)
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
            (r'/vintner', VintnerBaseHandler),
            (r'/vintner/(\d+)', VintnerHandler),
            (r'/vintner/(\d+)/wine', VintnerWineBaseHandler),
            (r'/vintner/(\d+)/wine/(\d+)', VintnerWineHandler),
            (r'/search', SearchHandler),
        ]
