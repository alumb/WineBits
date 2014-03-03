from truth.stubs import webapp2, ndb
from truth.views.jsonview import json_response
from truth.models.winebottle import WineBottle
from truth.constants import MAX_RESULTS
from truth.models.wine import Wine
from truth.models.winery import Winery
from truth.models.cellar import WineCellar
from truth.models.event import Event
from truth.models.user import User


class WineBottleBaseHandler(webapp2.RequestHandler):
    def get(self, cellar_id=None):

        if cellar_id is None:
            cellar_id = User.get_current_user().cellar.id()

        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()

        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.has_access(cellar_key):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"
            return

        qry = WineBottle.query(ancestor=cellar.key)
        results = qry.fetch(MAX_RESULTS)

        json_response(self, results)

    def post(self, cellar_id=None):

        if cellar_id is None:
            cellar_id = User.get_current_user().cellar.id()

        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()

        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.has_access(cellar_key):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"
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
            
            Event.create(self.request.remote_addr, "WineBottle", key)

            self.response.content_type = "application/json"
            json_response(self, bottle)

        else:
            json_response(self, {"error": "there was no wine_id", "post": self.request.body})


class WineBottleHandler(webapp2.RequestHandler):

    # if winebottle_id is None, the winebottle_id is in cellar_id and the cellar_id is the cellar
    # of this user.
    def get(self, cellar_id, winebottle_id=None):

        if winebottle_id is None:
            winebottle_id = cellar_id
            cellar_id = User.get_current_user().cellar.id()

        bottle_key = ndb.Key(WineCellar, int(cellar_id), WineBottle, int(winebottle_id))
        bottle = bottle_key.get()

        if not bottle:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.has_access(ndb.Key(WineCellar, int(cellar_id))):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"
            return

        json_response(self, bottle)

    def post(self, cellar_id, winebottle_id=None):

        if winebottle_id is None:
            winebottle_id = cellar_id
            cellar_id = User.get_current_user().cellar.id()

        bottle_key = ndb.Key(WineCellar, int(cellar_id), WineBottle, int(winebottle_id))
        bottle = bottle_key.get()

        if not bottle:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.has_access(ndb.Key(WineCellar, int(cellar_id))):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"
            return

        post = self.request.POST

        if 'wine_id' in post and 'winery_id' in post:

            wine_key = ndb.Key(Winery, int(post['winery_id']), Wine, int(post['wine_id']))
            wine = wine_key.get()

            del post['wine_id']
            del post['winery_id']

            bottle.wine = wine.key

            key = bottle.modify(post)

            Event.update(self.request.remote_addr, "WineBottle", key)

            self.response.content_type = "application/json"
            json_response(self, bottle)

        else:
            json_response(self, {"error": "there was no wine_id", "post": self.request.body})

    def delete(self, cellar_id, winebottle_id=None):

        if winebottle_id is None:
            winebottle_id = cellar_id
            cellar_id = User.get_current_user().cellar.id()

        bottle_key = ndb.Key(WineCellar, int(cellar_id), WineBottle, int(winebottle_id))
        bottle = bottle_key.get()

        if not bottle:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.has_access(ndb.Key(WineCellar, int(cellar_id))):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"
            return
                    
        bottle.delete()

        Event.create(self.request.remote_addr, "WineBottle", bottle_key)

        json_response(self, {"success": True})
        
routes = [
    (r'/cellar/(\d+)/wine/?', WineBottleBaseHandler),
    (r'/cellar/wine/?', WineBottleBaseHandler),
    (r'/cellar/(\d+)/wine/(\d+)/?', WineBottleHandler),
    (r'/cellar/wine/(\d+)/?', WineBottleHandler),
]
