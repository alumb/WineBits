from truth.stubs import webapp2 
from truth.views.jsonview import json_response 
from truth import regions
from truth.models.winery import Winery

class LocationHandler(webapp2.RequestHandler):
    """
    GET /location : an exhaustive list of every location
    GET /location?fuzzy=true : every location_fuzzy
    """
    def get(self):
        if 'fuzzy' in self.request.GET:
            json_response(self, Winery.all_fuzzy_locations())
        else:
            json_response(self, regions.location_list)

routes = [
    (r'/location/?', LocationHandler),
]
