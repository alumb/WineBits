from truth.models.base import YouNeedATokenForThat
from truth.models.winery import Winery
from truth.models.wine import Wine
from truth.models.event import Event
from truth.stubs import webapp2, ndb, debug, search
from truth import regions, wine_types



class WineryBaseHandler(webapp2.RequestHandler):
    """
    GET /winery : fetch a set of winerys
    POST /winery : create a winery
    """

    def get(self):
        """
        /winery?
        /winery?country=Canada
        /winery?region=British Columbia
        /winery?subregion=Okanagan Valley
        /winery?name="Black Hills Estate"
        /winery?location="Canada - British Columbia: Okanagan Valley"
        /winery?location_fuzzy="Somewhere"
        """
        #TODO: Compound Queries
        get = self.request.GET
        if 'subregion' in get:
            self.json_response(Winery.subregion_query(get['subregion']))
            return
        if 'region' in get:
            self.json_response(Winery.region_query(get['region']))
            return
        if 'country' in get:
            self.json_response(Winery.country_query(get['country']))
            return
        if 'name' in get:
            self.json_response(Winery.name_query(get['name']))
            return
        if 'location' in get:
            self.json_response(Winery.location_query(get['location']))
            return
        if 'location_fuzzy' in get:
            self.json_response(Winery.location_fuzzy_query(
                               get['location_fuzzy']))
            return
        if 'verified_by' in get:
            self.json_response(Winery.verified_by_query(
                               get['verified_by']))
            return
        if 'verified' in get:
            verified = False
            if get['verified'].lower() == 'true':
                verified = True
            self.json_response(Winery.verified_query(verified))
            return

        #if no params, return entire list.
        self.json_response(Winery.all_query())

    def post(self):
        """

        >>> v = WineryBaseHandler()
        >>> v.request.POST = {'name':'Winery'}
        >>> v.post()
        >>> v.response.content_type
        'application/json'
        >>> v.response.last_write
        '{..."key": "stub-key"...}'

        """
        post = self.request.POST

        winery = Winery()
        try:
            key = winery.create(post)
            winery.update()
            Event.create(self.request.remote_addr, "Winery", key)
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.json_response(winery)


class WineryHandler(webapp2.RequestHandler):
    """
    /winery/<id>
    """

    def get(self, winery_id):
        """
        >>> v = Winery()
        >>> key = v.create({'name':'winery'})
        >>> ndb.Key.load_get(v )

        >>> h = WineryHandler()
        >>> h.get('12345')
        >>> h.response.content_type
        'application/json'
        >>> h.response.last_write
        '{..."name": "winery",..."key":...}'
        """

        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()
        if not winery:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        self.json_response(winery)

    def post(self, winery_id):
        """
        >>> v = Winery()
        >>> key = v.create({'name':'winery'})
        >>> ndb.Key.load_get(v )

        >>> h = WineryHandler()
        >>> h.request.POST = {'location':'Canada'}
        >>> h.post('12345')
        >>> h.response.content_type
        'application/json'
        >>> h.response.last_write
        '{..."country": "Canada"...}'
        >>> h.response.last_write
        '{..."name": "winery"...}'
        >>> h.response.last_write
        '{..."key":...}'
        """

        post = self.request.POST

        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        try:
            winery.modify(post)
            wines = Wine.winery_query(winery)
            winery.update(wines)
            Event.update(self.request.remote_addr, "Winery", winery_key)
        except YouNeedATokenForThat as e:
            self.response.write(str(e))
            self.response.status = "401 Unauthorized"
            return

        self.json_response(winery)


class WineryWineBaseHandler(webapp2.RequestHandler):
    def get(self, winery_id):
        """
        /winery/12345/wine => all wines for winery
        """
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        if not winery:
            self.response.write("404 Not Found")
            self.response.status = "404 Not Found"
            return

        self.json_response(Wine.winery_query(winery))

    def post(self, winery_id):
        """
        POST /winery/12345/wine => create a wine for winery
        """
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()

        if not winery:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        post = self.request.POST

        wine = Wine(parent=winery_key)
        try:
            key = wine.create( post, winery )
            wine.update(winery)
            Event.create(self.request.remote_addr, "Wine", key)
        except ValueError as e:
            self.response.status = "400 Bad Request"
            self.response.write(str(e))
            return

        self.json_response(wine)

class WineryWineHandler(webapp2.RequestHandler):
    def get(self, winery_id, wine_id):
        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        self.json_response(wine)

    def post(self, winery_id, wine_id):
        winery_key = ndb.Key(Winery, int(winery_id))
        winery = winery_key.get()
        wine_key = ndb.Key(Winery, int(winery_id), Wine, int(wine_id))
        wine = wine_key.get()

        if not winery or not wine:
            self.response.status = "404 Not Found"
            self.response.write("404 Not found." )
            return

        post = self.request.POST

        try:
            wine.modify(post, winery)
            wine.update(winery)
            Event.update(self.request.remote_addr, "Wine", wine_key)

        except YouNeedATokenForThat as e:
            self.response.write(str(e))
            self.response.status = "401 Unauthorized"
            return

        self.json_response(wine)



class SearchHandler(webapp2.RequestHandler):
    """
    /search
    """

    def get(self):
        if not 'q' in self.request.GET:
            query = ""
        else:
            query = self.request.GET['q']

        wine_index = search.Index(name="wines")
        winery_index = search.Index(name="wineries")
        
        wine_limiter = search.QueryOptions(
            returned_fields=['year', 'name', 'varietal', 'winery', 'varietal',
                            'winetype', 
                             'upc', 'verified', 'id', 'winery_id', 'rank']) 
        winery_limiter = search.QueryOptions(
            returned_fields=['name', 'location', 'verified', 'id', 'rank'])

        # this can throw a search.Error, which should be a 500, I think?
        wine_query = search.Query(query_string=query, options=wine_limiter)
        winery_query = search.Query(query_string=query, options=winery_limiter)

        wine_results = wine_index.search(wine_query)
        winery_results = winery_index.search(winery_query)
       
        def to_dict(doc):
            dict_ = {}
            for field in doc.fields:
                try:
                    dict_[field.name] = int(field.value)
                except:
                    dict_[field.name] = str(field.value)
            return dict_
        
        def with_url(dict_):
            if 'id' in dict_ and not 'winery_id' in dict_:
                dict_['url'] = "/winery/"+str(dict_['id'])
            elif 'id' in dict_ and 'winery_id' in dict_:
                dict_['url'] = ( "/winery/"+str(dict_['winery_id']) +
                                 "/wine/"+str(dict_['id']) )
            return dict_


        wines = [with_url(to_dict(wine)) for wine in wine_results.results]
        wineries = [with_url(to_dict(winery)) for winery 
                                                in winery_results.results]

        response = {'wines':wines, 'wineries':wineries }
        
        self.json_response(response)


            (r'/winery/?', WineryBaseHandler),
            (r'/winery/(\d+)/?', WineryHandler),
            (r'/winery/(\d+)/wine/?', WineryWineBaseHandler),
            (r'/winery/(\d+)/wine/(\d+)/?', WineryWineHandler),
            (r'/search', SearchHandler),
        ]
