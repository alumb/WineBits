import os

import views
from stubs import debug, webapp2

if debug:
    print "Debug mode enabled, bitches."

routes = views.routes

application = webapp2.WSGIApplication(routes=routes, debug=debug, config={})
