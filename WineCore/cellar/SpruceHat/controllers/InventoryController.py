from cellar.SpruceHat.stubs import debug, webapp2, ndb
from cellar.SpruceHat.views.JsonView import JsonView
from cellar.SpruceHat.models.WineBottle import WineBottle
from cellar.SpruceHat.constants import MAX_RESULTS
from google.appengine.api import users

import json

class InventoryHandler(webapp2.RequestHandler):
    def get(self):
        
        qry = WineBottle.query()        
        results = qry.fetch(MAX_RESULTS)

        JsonView.json_response(self, [x.to_JSON() for x in results])


class WineBottleHandler(webapp2.RequestHandler):         
    def get(self,wine_bottle_key_urlsafe):

        wine_bottle_key = ndb.Key(urlsafe=wine_bottle_key_urlsafe)
        wine_bottle = wine_bottle_key.get()

        if wine_bottle:
            jsondict = wine_bottle.to_dict()
            jsondict["wine"] = wine_bottle_key.parent().get().to_dict()
            jsondict["winery"] = wine_bottle_key.parent().parent().get().to_dict()
            JsonView.json_response(self, jsondict)



    def post(self):

        user = users.get_current_user()

        wine_key = ndb.Key(urlsafe='agxkZXZ-d2luZWJpdHNyJAsSBldpbmVyeRiAgICAgICACgwLEgRXaW5lGICAgICAgKAJDA')
        wine = wine_key.get()

        wineBottle = WineBottle(parent=wine_key)

        key = wineBottle.create({
                "yearBought":1900,
                "drinkBefor":1903   
            })

        wineBottle.yearBought = 2000

        self.response.content_type="application/json"
        jsondict = wineBottle.to_dict()
        jsondict["wine"] = wine.to_dict()
        
        JsonView.json_response(self, jsondict)
        
routes = [
    (r'/inventory/?', InventoryHandler), 
    (r'/inventory/([^/]*)/?', WineBottleHandler), 
]
