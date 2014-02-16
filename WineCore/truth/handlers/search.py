from truth.stubs import webapp2, search
from truth.views.jsonview import json_response


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
                dict_['url'] = "/winery/" + str(dict_['id'])
            elif 'id' in dict_ and 'winery_id' in dict_:
                dict_['url'] = ("/winery/" + str(dict_['winery_id']) +
                                "/wine/" + str(dict_['id']))
            return dict_

        wines = [with_url(to_dict(wine)) for wine in wine_results.results]
        wineries = [with_url(to_dict(winery)) for winery in winery_results.results]

        response = {'wines': wines, 'wineries': wineries}
        
        json_response(self, response)

routes = [
    (r'/search', SearchHandler),
]
