from truth.stubs import webapp2, ndb
from truth.views.jsonview import json_response 
from truth.models.event import Event
from truth.models.cellar import WineCellar

class CellarBaseHandler(webapp2.RequestHandler):
    def post(self):
        post = self.request.POST

        cellar = WineCellar()
        try:
            key = cellar.create(post)
            #Event.create(self.request.remote_addr, "WineCellar", key)
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

        json_response(self, cellar)

    def post(self, cellar_id):
        post = self.request.POST

        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()
        cellar.modify(post)
        #Event.create(self.request.remote_addr, "WineCellar", key)

        json_response(self, cellar)

    def delete(self, cellar_id):
        cellar_key = ndb.Key(WineCellar, int(cellar_id))
        cellar = cellar_key.get()
        cellar.delete()
        json_response(self, {"success":True})

routes = [
    (r'/cellar/?', CellarBaseHandler),
    (r'/cellar/([^/]*)/?', CellarHandler)
]

#### urls ####
# - update: POST /truth/cellar/_cellar-id_
# - delete: DELETE /truth/cellar/_cellar-id_
