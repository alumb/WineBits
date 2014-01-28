from truth.stubs import debug, webapp2, ndb
from truth.views.jsonview import json_response 
from truth.models.winebottle import WineBottle
from truth.constants import MAX_RESULTS
from google.appengine.api import users
from truth.models.wine import Wine
from truth.models.winery import Winery

import json

class InventoryHandler(webapp2.RequestHandler):
    def get(self):
        
        qry = WineBottle.query()        
        results = qry.fetch(MAX_RESULTS)

        JsonView.json_response(self, [x.to_JSON() for x in results])

    def post(self):

        user = users.get_current_user()

        post = self.request.POST

        if 'wine_id' in post and 'winery_id' in post:

            wine_key = ndb.Key(Winery, int(post['winery_id']), Wine, int(post['wine_id']))
            wine = wine_key.get()
            #wine = WineBottle.query(Wine.ID == int(wine_id))

            del post['wine_id']
            del post['winery_id']

            wineBottle = WineBottle(parent=wine_key)

            key = wineBottle.create(post)

            self.response.content_type="application/json"
            jsondict = wineBottle.to_dict()
            jsondict["wine"] = wine.to_dict()
            
            json_response(self, jsondict)

        else:
            json_response(self, {"error":"there was no wine_id","post":self.request.body})

    def delete(self):
        # post = json.loads(self.request.body)[0]

        # if 'wine_id' in post and 'winery_id' in post:

        #     wine_key = ndb.Key(Winery, int(post['winery_id']), Wine, int(post['wine_id']))
        #     wine = wine_key.get()
            
        #     json_response(self, {"success":True})

        # else:
            json_response(self, {"success":False})

class WineBottleHandler(webapp2.RequestHandler):         
    def get(self,wine_bottle_key_urlsafe):

        wine_bottle_key = ndb.Key(urlsafe=wine_bottle_key_urlsafe)
        wine_bottle = wine_bottle_key.get()

        if wine_bottle:
            jsondict = wine_bottle.to_dict()
            jsondict["wine"] = wine_bottle_key.parent().get().to_dict()
            jsondict["winery"] = wine_bottle_key.parent().parent().get().to_dict()
            json_response(self, jsondict)



        
routes = [
    (r'/inventory/?', InventoryHandler), 
    (r'/inventory/([^/]*)/?', WineBottleHandler), 
]
