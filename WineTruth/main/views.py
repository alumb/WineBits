from models import Vintner, YouNeedATokenForThat
import regions

import os
import json

from stubs import webapp2, ndb, debug


class MyHandler(webapp2.RequestHandler):
    @staticmethod
    def json(model):
        try:
            object_ = model.to_dict()
            if object_ and 'json' in object_ and object_['json']:
                for key, value in object_['json']:
                    object_[key] = value
                del object_['json']
            if isinstance(model, Vintner):
                object_['link'] = "/vintner/%d" % model.key.id()
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
    @staticmethod
    def vintner_link(location):
        return "/vintner?location=%s" % location

    @staticmethod
    def fuzzy_vintner_link(location):
        return "/vintner?location_fuzzy=%s" % location

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
    @staticmethod
    def vintner_link(country):
        return "/vintner?country=%s" % country

    @staticmethod
    def region_link(country):
        return "/country/%s" % country

    def get(self):
        response = [{
            'country':country,
            'regions':CountryHandler.region_link(country),
            'vintners':CountryHandler.vintner_link(country)}
            for country in regions.countries]
        self.json_response(response)

class RegionHandler(MyHandler):
    """
    GET /country/Canada : list regions
    """
    @staticmethod
    def vintner_link(region):
        return "/vintner?region=%s" % region

    @staticmethod
    def subregion_link(country, region):
        return "/country/%s/%s" % (country, region)

    def get(self, country):
        response = [{
            'region':region,
            'subregions':RegionHandler.subregion_link(country, region),
            'vintners':RegionHandler.vintner_link(region)}
            for region in regions.regions_for_country(country)]
        self.json_response(response)

class SubRegionHandler(MyHandler):
    """
    GET /country/Canada/British Columbia : list subregions
    """
    @staticmethod
    def vintner_link(subregion):
        return "/vintner?subregion=%s" % subregion

    def get(self, country):
        response = [{
            'subregion':subregion,
            'vintners':SubRegionHandler.vintner_link(subregion)}
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
