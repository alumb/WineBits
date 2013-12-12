import wine_types
from models.base import BaseModel, YouNeedATokenForThat
from models.winery import Winery

from stubs import ndb

class Wine(BaseModel):
    # Parent: Winery
    year = ndb.IntegerProperty()
    name = ndb.StringProperty()
    winetype = ndb.StringProperty(required=True, choices=wine_types.types)
    varietal = ndb.StringProperty()
    upc = ndb.StringProperty()

    @property
    def has_year(self):
        return self.has_key('year')

    @property
    def has_name(self):
        return self.has_key('name')

    @property
    def has_winetype(self):
        return self.has_key('winetype')

    @property
    def has_varietal(self):
        return self.has_key('varietal')

    @property
    def has_upc(self):
        return self.has_key('upc')

    verified = ndb.BooleanProperty(default=False)
    verified_by = ndb.StringProperty()

    json = ndb.JsonProperty(indexed=False)
    # JSON properties encompass the bits that might want to be tracked
    # but are too fiddly to keep track of regularly, like
    # bud_break, veraison, oak_regime, barrel_age, harvest_date,
    # bottling_date, alcohol_content, winemaker_notes, vineyard_notes...

    def has_json(self):
        return self.has_key('json')

    def create(self, post, winery):
        """

        >>> v = Winery()
        >>> v_key = v.create({'name':'Winery'})
        >>> w = Wine(parent=v_key)
        >>> post = {}
        >>> post['name'] = 'Red Character'
        >>> post['varietal'] = 'Blend'
        >>> post['winetype'] = 'Red'
        >>> post['upc'] = '1234567890'
        >>> post['blend'] = ['Merlot', 'Cabernet Franc']
        >>> post['token'] = "stub-uuid"
        >>> w_key = w.create(post, v)

        >>> w.name
        'Red Character'
        >>> w.varietal
        'Blend'
        >>> w.winetype
        'Red'
        >>> w.to_dict()['json']['blend']
        ['Merlot', 'Cabernet Franc']
        >>> w.verified
        True
        >>> w.verified_by
        'Winery'

        """
        name = None
        if 'name' in post:
            name = post['name']
            self.name = name
            del post['name']

        year = None
        if 'year' in post:
            year = int(post['year'])
            self.year = year
            del post['year']

        winetype = None
        if 'winetype' in post:
            winetype = post['winetype']
            if not winetype in wine_types.types:
                raise ValueError("Invalid Wine Type: " + str(winetype))
            else:
                self.winetype = winetype
                del post['winetype']

        varietal = None
        if 'varietal' in post:
            varietal = post['varietal']
            self.varietal = varietal
            del post['varietal']

        upc = None
        if 'upc' in post:
            upc = post['upc']
            del post['upc']

        if not winetype:
            raise ValueError("You must provide a winetype")

        if not name and not year and not varietal and not upc:
            raise ValueError("You must provide a name, year, "+
                             " varietal, or upc.")

        token = None
        if 'token' in post:
            token = post['token']
            self.verify(token, winery)
            del post['token']

        json = BaseModel.tidy_up_the_post_object(post)
        self.json = json

        key = self.put()
        return key

    def update(self, post, winery):
        """
        >>> v = Winery()
        >>> v_key = v.create({"name":"Winery"})
        >>> w = Wine(parent=v_key)
        >>> w_key = w.create({"winetype":"Red", "year":"2010"}, v)

        The base case.
        >>> w.update({"name":"Red Character", "terroir":"Good"}, v)
        >>> w.to_dict()["name"]
        'Red Character'

        >>> w.to_dict()["json"]["terroir"]
        'Good'

        >>> w2 = Wine(parent=v_key)
        >>> w2.update({"winetype":"White", "year":"2011"}, v)
        >>> w2.to_dict()["winetype"]
        'White'

        >>> w2.to_dict()["year"]
        2011

        >>> w.update({"varietal":"Blend"}, v)
        >>> w.to_dict()["varietal"]
        'Blend'

        >>> w.update({"upc":"123456789"}, v)
        >>> w.to_dict()["upc"]
        '123456789'

        You can't replace a field.
        >>> w.update({"winetype":"White"}, v)
        Traceback (most recent call last):
        ...
        YouNeedATokenForThat...

        >>> w.update({"terroir": "at danger lake!"}, v)
        Traceback (most recent call last):
        ...
        YouNeedATokenForThat...

        Should be fine if you update a thing with itself.
        >>> w.update({"winetype":"Red"}, v)
        >>> w.update({"terroir":"Good"}, v)

        You can update whatever you like if you have a token.
        >>> w.update({"winetype":"White", "token":"stub-uuid"}, v)
        >>> w.to_dict()["winetype"]
        'White'

        """
        def field_edit_error(fieldname):
            return YouNeedATokenForThat(("You can't edit fields that already" +
                                          " exist: %s" % fieldname))

        can_edit_fields = False
        if 'token' in post:
            token = post['token']
            can_edit_fields = self.verify(token, winery)
            del post['token']

        def can_edit_field(field_name):
            if field_name in post:
                if not self.has_key(field_name):
                    return True
                if post[field_name] == str(self.to_dict()[field_name]):
                    return True
                if can_edit_fields:
                    return True
                raise field_edit_error(field_name)
            else:
                return False

        name = None
        if can_edit_field('name'):
            name = post['name']
            self.name = name
            del post['name']

        year = None
        if can_edit_field('year'):
            year = int(post['year'])
            self.year = year
            del post['year']

        winetype = None
        if can_edit_field('winetype'):
            winetype = post['winetype']
            if not winetype in wine_types.types:
                raise ValueError("Invalid Wine Type: " + str(winetype))
            else:
                self.winetype = winetype
                del post['winetype']

        varietal = None
        if can_edit_field('varietal'):
            varietal = post['varietal']
            self.varietal = varietal
            del post['varietal']

        upc = None
        if can_edit_field('upc'):
            upc = post['upc']
            self.upc = upc
            del post['upc']

        json = BaseModel.tidy_up_the_post_object(post)
        if 'json' in self.to_dict():
            new_json = self.to_dict()['json']
            for key, value in json.iteritems():
                if key in new_json and can_edit_fields:
                    new_json[key] = value
                if not (key in new_json):
                    new_json[key] = value
                if key in new_json and new_json[key] == value:
                    pass
                else:
                    raise field_edit_error(key)
            self.json = new_json
        else:
            self.json = json

        key = self.put()
        return None

    def calculate_rank(self):
        rank = 0
        if self.has_year:
            rank += 2
        if self.has_name:
            rank += 2
        if self.has_winetype:
            rank += 2
        if self.has_varietal:
            rank += 4
        if self.has_upc:
            rank += 8
        if self.has_json:
            for key in self.to_dict()['json']:
                rank += 1
        return rank

    def verify(self, token=None, winery=None):
        """
        Sets self.verified and self.verified_by,
        True if the token is valid
        False if not
        """
        if not token:
            return False
        if winery and token == winery.private_token:
            self.verified = True
            self.verified_by = "Winery"
            return True
        return False

    @staticmethod
    def winery_query(winery):
        qry = Wine.query(ancestor=winery.key)
        results = qry.fetch(MAX_RESULTS)
        return [x for x in results]
