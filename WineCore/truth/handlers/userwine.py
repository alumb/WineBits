from truth.stubs import webapp2, ndb
from truth.views.jsonview import json_response 
from truth.models.event import Event
from truth.models.winery import Winery
from truth.models.wine import Wine
from truth.models.userwine import UserWine
from truth.constants import MAX_RESULTS
from truth.models.user import User


class UserWineBaseHandler(webapp2.RequestHandler):
    def get(self, winery_id, wine_id):

        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not wine:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        qry = UserWine.query(ancestor=wine_key)
        results = qry.fetch(MAX_RESULTS)

        json_response(self, [x for x in results])

    def post(self,winery_id,wine_id):
        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))

        post = self.request.POST

        userwine = UserWine(parent=wine_key)

        try:
            post['user'] = User.get_current_user()
            key = userwine.create(post)
            Event.create(self.request.remote_addr, "UserWine", key)
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        json_response(self, userwine)

class UserWineHandler(webapp2.RequestHandler):
    def get(self, winery_id, wine_id, userwine_id):

        userwine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id))
        userwine = userwine_key.get()
        if not userwine:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if userwine.user != User.get_current_user().key:
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"            
            return

        json_response(self, userwine)

    def post(self, winery_id, wine_id, userwine_id):
        post = self.request.POST

        userwine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id))
        userwine = userwine_key.get()
        if not userwine:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if userwine.user != User.get_current_user().key:
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"            
            return

        userwine.modify(post)
        Event.update(self.request.remote_addr, "UserWine", userwine_key)

        json_response(self, userwine)

    def delete(self, winery_id, wine_id, userwine_id):
        userwine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id), UserWine, int(userwine_id))
        userwine = userwine_key.get()
        if not userwine:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if userwine.user != User.get_current_user().key:
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"            
            return

        userwine.delete()
        json_response(self, {"success":True})

routes = [
    (r'/winery/(\d+)/wine/(\d+)/userwine/?', UserWineBaseHandler),
    (r'/winery/(\d+)/wine/(\d+)/userwine/(\d+)/?', UserWineHandler),
]
