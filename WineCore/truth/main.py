from truth.handlers import root, location, varietal, winetype, region, winery, debug_handler
from truth.handlers import wine, userwine, winetasting, search, cellar, winebottle
from truth.stubs import debug, webapp2

if debug:
    print "Debug mode enabled, bitches."

base = "/truth"

handler_modules = [
    root,
    location,
    varietal,
    winetype,
    region,
    winery,
    wine,
    userwine,
    winetasting,
    search,
    winebottle,
    cellar,
    debug_handler
]

routes = []
for module in handler_modules:
    for route, handler in module.routes:
        routes.append((base + route, handler))

application = webapp2.WSGIApplication(routes=routes, debug=debug, config={})
