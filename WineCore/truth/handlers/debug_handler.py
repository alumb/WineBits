from truth.stubs import webapp2
from truth.views.jsonview import json_response 
from truth.constants import MAX_RESULTS
from truth.models.user import User



class userMapHandler(webapp2.RequestHandler):
    def get(self):
        qry = User.query()
        results = qry.fetch(MAX_RESULTS)        
        
        json_response(self, [user for user in results])


routes = [
    (r'/debug/usermap/?', userMapHandler),
]
