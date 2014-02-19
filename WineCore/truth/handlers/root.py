from truth.stubs import webapp2


class BaseHandler(webapp2.RequestHandler):
    """
    / : returns a 'hello' sort of deal.
    """

    def get(self):
        self.response.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>WineBits: WineTruth</title>
    <link rel="stylesheet" href="/style/css/bootstrap.min.css" />
    <script src="/style/js/bootstrap.min.js"></script>
    <link href='http://fonts.googleapis.com/css?family=Roboto+Slab:400,100,700,300'
            rel='stylesheet' type='text/css'>
  </head>
  <body>
    <h1> Welcome to WineTruth. </h1>
    <p> The documentation is available
    <a href='https://github.com/alumb/WineBits/blob/master/WineCore/truth/README.md'>here</a></p>
  </body>
</html>
            """)


routes = [(r'/', BaseHandler)]
