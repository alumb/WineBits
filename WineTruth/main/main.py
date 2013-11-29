import webapp2
import os

import views

#try:
#    from google.appengine.api import channel
#except ImportError:
#    from stubs import channel
# The most basic WSGI application
#def application(environ, start_response):
#    start_response('200 OK', [('Content-Type', 'application/json')])
#    return [json.dumps(channel.create_channel("hobo-fight") )]

debug=os.environ["DEBUG"]

if debug:
    print "Debug mode enabled, bitches."

application = webapp2.WSGIApplication(routes=views.routes, debug=debug, config={})
