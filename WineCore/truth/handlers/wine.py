from truth.models.base import YouNeedATokenForThat
from truth.stubs import webapp2, ndb
from truth.views.jsonview import json_response
from truth.models.wine import Wine
from truth.models.winery import Winery
from truth.models.event import Event


class WineryWineBaseHandler(webapp2.RequestHandler):
    def get(self, winery_id):
        """
        /winery/12345/wine => all wines for winery
        """
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        if not winery:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        json_response(self, Wine.winery_query(winery))

    def post(self, winery_id):
        """
        POST /winery/12345/wine => create a wine for winery
        """
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        if not winery:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found.")
            return

        post = self.request.POST

        wine = Wine(parent=winery_key)
        try:
            key = wine.create(post, winery)
            wine.update(winery)
            Event.create(self.request.remote_addr, "Wine", key)
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        json_response(self, wine)


class WineryWineHandler(webapp2.RequestHandler):
    def get(self, winery_id, wine_id):
        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found.")
            return

        json_response(self, wine)

    def post(self, winery_id, wine_id):
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()
        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not winery or not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found.")
            return

        post = self.request.POST

        try:
            wine.modify(post, winery)
            wine.update(winery)
            Event.update(self.request.remote_addr, "Wine", wine_key)

        except YouNeedATokenForThat as e:
            self.response.write(str(e))
            self.response.status = "401 Unauthorized"
            return

        json_response(self, wine)


routes = [
    (r'/winery/(\d+)/wine/?', WineryWineBaseHandler),
    (r'/winery/(\d+)/wine/(\d+)/?', WineryWineHandler),
]
