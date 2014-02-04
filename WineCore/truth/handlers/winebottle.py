from truth.stubs import debug, webapp2, ndb
from truth.views.jsonview import json_response 
from truth.models.winebottle import WineBottle
from truth.constants import MAX_RESULTS
from google.appengine.api import users
from truth.models.wine import Wine
from truth.models.winery import Winery
from truth.models.cellar import WineCellar

import json

class WineBottleBaseHandler(webapp2.RequestHandler):
    def get(self, cellar_id):
        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()

        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        qry = WineBottle.query(ancestor=cellar.key)        
        results = qry.fetch(MAX_RESULTS)

        json_response(self, results, True)

    def post(self, cellar_id):

        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()

        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        post = self.request.POST

        if 'wine_id' in post and 'winery_id' in post:

            wine_key = ndb.Key(Winery, int(post['winery_id']), Wine, int(post['wine_id']))
            wine = wine_key.get()

            del post['wine_id']
            del post['winery_id']

            bottle = WineBottle(parent=cellar_key)
            bottle.wine = wine.key

            key = bottle.create(post)

            self.response.content_type="application/json"
            json_response(self, bottle)

        else:
            json_response(self, {"error":"there was no wine_id","post":self.request.body})

class WineBottleHandler(webapp2.RequestHandler):         
    def get(self,cellar_id,winebottle_id):

        bottle_key = ndb.Key(WineCellar, int(cellar_id), WineBottle, int(winebottle_id))
        bottle = bottle_key.get()

        if not bottle:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        json_response(self, bottle)

    def post(self,cellar_id,winebottle_id):
        bottle_key = ndb.Key(WineCellar, int(cellar_id), WineBottle, int(winebottle_id))
        bottle = bottle_key.get()

        if not bottle:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        post = self.request.POST

        if 'wine_id' in post and 'winery_id' in post:

            wine_key = ndb.Key(Winery, int(post['winery_id']), Wine, int(post['wine_id']))
            wine = wine_key.get()

            del post['wine_id']
            del post['winery_id']

            bottle.wine = wine.key

            key = bottle.modify(post)

            self.response.content_type="application/json"
            json_response(self, bottle)

        else:
            json_response(self, {"error":"there was no wine_id","post":self.request.body})

    def delete(self,cellar_id,winebottle_id):

        bottle_key = ndb.Key(WineCellar, int(cellar_id), WineBottle, int(winebottle_id))
        bottle = bottle_key.get()

        if not bottle:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return
        
        bottle.delete()

        json_response(self, {"success":True})
        
routes = [
    (r'/cellar/(\d+)/wine/?', WineBottleBaseHandler), 
    (r'/cellar/(\d+)/wine/(\d+)/?', WineBottleHandler), 
]
