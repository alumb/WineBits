from truth.handlers import root, location, varietal, winetype, region
from truth.stubs import debug, webapp2

if debug:
    print "Debug mode enabled, bitches."

base= "/truth"

handler_modules = [
    root,
    location,
    varietal,
    winetype, 
    region
]

routes = []
for module in handler_modules: 
    for route, handler in module.routes:
        routes.append(( base + route, handler ))

application = webapp2.WSGIApplication(routes=routes, debug=debug, config={})
