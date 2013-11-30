from models import Vintner, Wine, YouNeedATokenForThat
import regions

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
    if 'location' in dict_:
        location = dict_['location']
        dict_['vintner_location'] = "/vintner?location=%s" % location
    if 'location_fuzzy' in dict_:
        location = dict_['location_fuzzy']
        dict_['vintner_location_fuzzy'] = "/vintner?location_fuzzy=%s" % location
    if 'country' in dict_:
        country = dict_['country']
        dict_['vintner_country'] = "/vintner?country=%s" % country
        dict_['country_regions'] = "/country/%s" % country
    if 'region' in dict_ and 'country' in dict_:
        region = dict_['region']
        country = dict_['country']
        dict_['vintner_region'] = "/vintner?region=%s" % region
        dict_['region_subregions'] = "/country/%s/%s" % (country, region)
    if 'subregion' in dict_:
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
    def get(self):
        if 'fuzzy' in self.request.GET:
            response = [{
                'location':location,
                'vintners':LocationHandler.fuzzy_vintner_link(location)}
                for location in Vintner.all_fuzzy_locations()]

            self.json_response(response)
        else:
            response = [{
                'location':location,
                'vintners':LocationHandler.vintner_link(location)}
                for location in regions.location_list]

            self.json_response(response)

class CountryHandler(MyHandler):
    """
    GET /country : list countries
    """
    def get(self):
        response = [{'country':country} for country in regions.countries]
        self.json_response(response)

class RegionHandler(MyHandler):
    """
    GET /country/Canada : list regions
    """

    def get(self, country):
        response = [{'region':region,'country':country}
                    for region in regions.regions_for_country(country)]
        self.json_response(response)

class SubRegionHandler(MyHandler):
    """
    GET /country/Canada/British Columbia : list subregions
    """

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
        self.response.write(key.id())


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


class VintnerWineBaseHandler(webapp2.RequestHandler):
    def get(self, vintner_id):
        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()
        self.response.write("Wines for vintner")

    def post(self, vintner_id):
        vintner_key = ndb.Key(Vintner, int(vintner_id))
        vintner = vintner_key.get()

        if not vintner:
            self.response.status = "400 Bad Request"
            self.response.write("Vintner not found." )
            return

        post = self.request.POST

        wine = Wine(parent=vintner_key)
        try:
            key = wine.create( post, vintner )
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.response.content_type="text/plain"
        self.response.write(key)


class VintnerWineHandler(webapp2.RequestHandler):
    def get(self, vintner_id, wine_id):
        pass


class SearchHandler(webapp2.RequestHandler):
    """
    /search
    """

    def get(self):
        pass


routes = [
            (r'/location', LocationHandler),
            (r'/country', CountryHandler),
            (r'/country/([\w\s\d%]+)', RegionHandler),
            (r'/country/([\w\s\d%]+)/([\w\s\d%]+)', SubRegionHandler),
            (r'/vintner', VintnerBaseHandler),
            (r'/vintner/(\d+)', VintnerHandler),
            (r'/vintner/(\d+)/wine', VintnerWineBaseHandler),
            (r'/vintner/(\d+)/wine/(\d+)', VintnerWineHandler),
            (r'/search', SearchHandler),
        ]
