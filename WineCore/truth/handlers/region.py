from truth.stubs import webapp2 
from truth.views.jsonview import json_response 
from truth import regions

class CountryHandler(webapp2.RequestHandler):
    """
    GET /country : list countries
    """
    def get(self):
        json_response(self, regions.countries)

class RegionHandler(webapp2.RequestHandler):
    """
    GET /country/Canada : list regions
    """

    def get(self, country):
        json_response(self, regions.regions_for_country(country))

class SubRegionHandler(webapp2.RequestHandler):
    """
    GET /country/Canada/British Columbia : list subregions
    """

    def get(self, country, region):
        json_response(self, regions.subregions_for_country(country, region))
        
routes = [
    (r'/country/?', CountryHandler),
    (r'/country/([\w\s\d%]+)/?', RegionHandler),
    (r'/country/([\w\s\d%]+)/([\w\s\d%]+)/?', SubRegionHandler)
]
