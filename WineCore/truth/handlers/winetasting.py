from truth.stubs import webapp2, ndb
from google.appengine.api import users
from truth.views.jsonview import json_response 
from truth.constants import MAX_RESULTS
from truth.models.event import Event
from truth.models.winery import Winery
from truth.models.wine import Wine
from truth.models.userwine import UserWine
from truth.models.winetasting import WineTasting

import logging
from datetime import datetime

class WineTastingBaseHandler(webapp2.RequestHandler):
    def get(self,winery_id,wine_id,userwine_id):
        userwine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id))
        userwine = userwine_key.get()

        if not userwine:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        qry = WineTasting.query(ancestor=userwine.key)        
        results = qry.fetch(MAX_RESULTS)

        json_response(self, results, True)

    def post(self,winery_id,wine_id,userwine_id):
        userwine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id))

        post = self.request.POST

        tasting = WineTasting(parent=userwine_key)

        try:
            key = tasting.create(post)
            Event.create(self.request.remote_addr, "WineTasting", key)
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        json_response(self, tasting)

class WineTastingHandler(webapp2.RequestHandler):
    def get(self, winery_id, wine_id, userwine_id, tasting_id):

        tasting_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id), WineTasting, int(tasting_id))
        tasting = tasting_key.get()
        if not tasting:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        json_response(self, tasting)

    def post(self, winery_id, wine_id, userwine_id, tasting_id):
        post = self.request.POST

        tasting_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id), WineTasting, int(tasting_id))
        tasting = tasting_key.get()
        tasting.modify(post)
        #Event.create(self.request.remote_addr, "WineTasting", key)

        json_response(self, tasting)

    def delete(self, winery_id, wine_id, userwine_id, tasting_id):
        tasting_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id), WineTasting, int(tasting_id))
        tasting = tasting_key.get()
        tasting.delete()
        json_response(self, {"success":True})

routes = [
    (r'/winery/(\d+)/wine/(\d+)/userwine/(\d+)/tasting?', WineTastingBaseHandler),
    (r'/winery/(\d+)/wine/(\d+)/userwine/(\d+)/tasting/(\d+)/?', WineTastingHandler),
]
