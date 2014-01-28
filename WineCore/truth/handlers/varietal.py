from truth.stubs import webapp2 
from truth.views.jsonview import json_response 
from truth import wine_types

class VarietalHandler(webapp2.RequestHandler):
    """
    /varietal : all varietals
    """
    def get(self):
        response = [varietal
                    for varietal in wine_types.wine_options]
        json_response(self, response)

routes = [
            (r'/varietal/?', VarietalHandler),

        ]
