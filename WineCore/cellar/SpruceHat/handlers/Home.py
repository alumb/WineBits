from cellar.SpruceHat.stubs import webapp2, ndb, debug, search
from google.appengine.api import users

import os
import json


class HomeHandler(webapp2.RequestHandler):
    """
    / : returns a 'hello' sort of deal. 
    """

    def get(self):
        user = users.get_current_user()

        self.response.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>WineBits: WineCellar</title>
    <link rel="stylesheet" href="/style/css/bootstrap.min.css" />
    <script src="/style/js/bootstrap.min.js"></script>
    <link href='http://fonts.googleapis.com/css?family=Roboto+Slab:400,100,700,300' rel='stylesheet' type='text/css'>
  </head>
  <body>
    <h1> Welcome to WineCellar.</h1>
    <p> hello: """ + user.nickname() + """</p>
    <p> Sign-out: <a href=\"""" + users.create_logout_url("") + """\">Logout</a> </p>
  </body>
</html>
                """)

routes = [
            (r'/', HomeHandler), 
        ]
