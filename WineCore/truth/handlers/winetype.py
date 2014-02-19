from truth.stubs import webapp2
from truth.views.jsonview import json_response
from truth import wine_types


class WineTypeHandler(webapp2.RequestHandler):
    """
    /winetype : all wine-types
    """
    def get(self):
        json_response(self, wine_types.types)


routes = [
    (r'/winetype/?', WineTypeHandler),
]
