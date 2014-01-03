from stubs import debug, webapp2
from controllers import HomeController
from controllers import InventoryController

if debug:
    print "Debug mode enabled, bitches."

base= "/cellar/server"

routes = []
routes.extend([(base + route, handler) for route, handler in HomeController.routes])
routes.extend([(base + route, handler) for route, handler in InventoryController.routes])

application = webapp2.WSGIApplication(routes=routes, debug=debug, config={})
