from cellar.SpruceHat import views
from cellar.SpruceHat.stubs import debug, webapp2

if debug:
    print "Debug mode enabled, bitches."

base= "/cellar/server"

routes = [(base + route, handler) for route, handler in views.routes]

application = webapp2.WSGIApplication(routes=routes, debug=debug, config={})
