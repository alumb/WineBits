from truth.stubs import webapp2, ndb
from truth.views.jsonview import json_response 
from truth.constants import MAX_RESULTS
from truth.models.event import Event
from truth.models.cellar import WineCellar
from truth.models.user import User
from truth.models.winebottle import WineBottle

class CellarBaseHandler(webapp2.RequestHandler):
    def get(self):
        cellar_key = User.get_current_user().cellar
        if cellar_key == None:
            return json_response(self, [])
        cellar = cellar_key.get()
        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.hasAccess(cellar_key):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"            
            return
        
        json_response(self, cellar)

    def post(self):
        post = self.request.POST

        cellar = WineCellar()
        try:
            user = User.get_current_user()
            if user.cellar != None:
                self.response.write("403 Forbidden - User already has cellar")
                self.response.status = "403 Forbidden"
                return
            key = cellar.create(post)

            user.cellar = key
            user.put()

            Event.create(self.request.remote_addr, "WineCellar", key)
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        json_response(self, cellar)

class CellarHandler(webapp2.RequestHandler):
    def get(self, cellar_id):

        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()
        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.hasAccess(cellar_key):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"            
            return
        
        json_response(self, cellar)

    def post(self, cellar_id):
        post = self.request.POST

        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()
        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.hasAccess(cellar_key):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"            
            return

        cellar.modify(post)
        Event.update(self.request.remote_addr, "WineCellar", cellar_key)

        json_response(self, cellar)

    def delete(self, cellar_id):
        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()
        if not cellar:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        if not User.hasAccess(cellar_key):
            self.response.write("403 Forbidden")
            self.response.status = "403 Forbidden"            
            return

        qry = WineBottle.query(ancestor=cellar.key)        
        results = qry.fetch(MAX_RESULTS)
        for bottle in results:
            bottle.delete()

        cellar.delete()
        user = User.get_current_user()
        user.cellar = None
        user.put()
        Event.delete(self.request.remote_addr, "WineCellar", cellar_key)
        json_response(self, {"success":True})

routes = [
    (r'/cellar/?', CellarBaseHandler),
    (r'/cellar/([^/]*)/?', CellarHandler)
]

#### urls ####
# - update: POST /truth/cellar/_cellar-id_
# - delete: DELETE /truth/cellar/_cellar-id_
