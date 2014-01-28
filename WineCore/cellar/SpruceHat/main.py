from stubs import debug, webapp2
from handlers import Home
from handlers import Inventory

if debug:
    print "Debug mode enabled, bitches."

base= "/cellar/server"

routes = []
routes.extend([(base + route, handler) for route, handler in Home.routes])
routes.extend([(base + route, handler) for route, handler in Inventory.routes])

application = webapp2.WSGIApplication(routes=routes, debug=debug, config={})
