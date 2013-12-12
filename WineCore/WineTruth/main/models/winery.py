import copy

import regions
from models.base import BaseModel, YouNeedATokenForThat
from stubs import ndb, uuid, search
from constants import MAX_RESULTS

class Winery(BaseModel):
    """
    Represents a single wine producer.
    """
    name = ndb.StringProperty(required=True)

    location = ndb.StringProperty(choices=regions.location_list)
    location_fuzzy = ndb.StringProperty()

    @property
    def has_location(self):
        return self.has_key('location')

    @property
    def has_location_fuzzy(self):
        return self.has_key('location_fuzzy')

    # these fields are calculated from location
    # and can't be set from the web interface
    country = ndb.StringProperty(choices=regions.countries)
    region = ndb.StringProperty(choices=regions.regions)
    subregion = ndb.StringProperty(choices=regions.subregions)

    @property
    def has_country(self):
        return self.has_key('country')

    @property
    def has_region(self):
        return self.has_key('region')

    @property
    def has_subregion(self):
        return self.has_key('subregion')

    #security stuff
    verified = ndb.BooleanProperty(default=False)
    verified_by = ndb.StringProperty()
    private_token = ndb.StringProperty(indexed=False)

    rank = ndb.IntegerProperty(required=True, default=0)

    @property
    def has_verified(self):
        return self.has_key('verified')

    @property
    def has_verified_by(self):
        return self.has_key('verified_by')

    json = ndb.JsonProperty(indexed=False)

    @property
    def has_json(self):
        return self.has_key('json')
    # website, phone_number

    def create(self, post):
        """
        Given a dict 'post' object containing winery-y fields,
        populate and put this Winery object, return the key.

        Throws a ValueError if no 'name' is included.
        >>> v_for_winery = Winery()
        >>> v_for_winery.create({})
        Traceback (most recent call last):
        ...
        ValueError: 'name' field is mandatory

        Basic use-case test.
        >>> location = 'Canada - British Columbia: Okanagan Valley'
        >>> post = {'name':'Super Winery', 'location':location }
        >>> v_for_winery = Winery()
        >>> database_key = v_for_winery.create(post)
        >>> v_for_winery.country
        u'Canada'
        >>> v_for_winery.region
        u'British Columbia'
        >>> v_for_winery.subregion
        u'Okanagan Valley'
        >>> database_key.id()
        'stub-key'

        If the location isn't in our list, it goes into location_fuzzy
        >>> location = 'Other'
        >>> post = {'name':'Super Winery 2', 'location':location}
        >>> v_for_winery = Winery()
        >>> database_key = v_for_winery.create(post)
        >>> v_for_winery.to_dict()
        {...'location_fuzzy': 'Other', ...}
        >>> v_for_winery.to_dict()['location_fuzzy']
        'Other'

        Winerys get a private token, which doesn't appear in to_dict()
        >>> v_for_winery.private_token
        'stub-uuid'
        >>> v_for_winery.to_dict()['private_token']
        Traceback (most recent call last):
        ...
        KeyError: 'private_token'

        Fields that we don't have database rows for go into the JSON.
        >>> post = {'name':'Super Winery 3', 'other_field':'glerg'}
        >>> v_for_winery = Winery()
        >>> database_key = v_for_winery.create(post)
        >>> v_for_winery.json
        {'other_field': 'glerg'}

        """
        if not 'name' in post:
            raise ValueError("'name' field is mandatory")
        name = post['name']
        self.name = name
        del post['name']

        if 'location' in post:
            location = post['location']
            self.set_location(location)
            del post['location']

        self.private_token = uuid.uuid4().hex

        # special: winerys + verifieds are magic
        if 'token' in post:
            self.verify(post['token'])
            del post['token']

        # having taken care of 'name' and 'location',
        # we wedge everything else into the JSON
        json = BaseModel.tidy_up_the_post_object(post)
        self.json = json

        self.rank = self.calculate_rank()

        key = self.put()
        return key

    def modify(self, post):
        """
        Given a dict 'post' object containing winery-y fields,
        update this object.

        Empty fields can always be updated. Fields cannot be overwritten
        without a valid winery or verifier token.

        If this object has been verified, no changes may occur without
        a valid winery or verifier token.

        Throws a YouNeedATokenForThat error if the user tries something
        he doesn't have access to without a token

        Let's create a Winery to update...
        >>> location = 'Canada - British Columbia: Okanagan Valley'
        >>> post = {'name':'Super Winery' }
        >>> post['location_fuzzy'] = 'Somewhere'
        >>> post['json_thing'] = 'blerg'
        >>> v = Winery()
        >>> v.location
        <stubs.StringProperty ...>
        >>> database_key = v.create(post)

        And update the location:
        >>> new_post = {'location':location}
        >>> new_post['json_other_thing'] = 'blorg'
        >>> v.modify(new_post)
        >>> v.country
        u'Canada'
        >>> v.to_dict()['json']['json_other_thing']
        'blorg'

        Updates of existing fields should fail.
        >>> other_location = 'Canada - British Columbia: Similkameen Valley'
        >>> v.modify({'location':other_location})
        Traceback (most recent call last):
        ...
        YouNeedATokenForThat...

        Updates of json fields that already exist should fail.
        >>> v.modify({'json_other_thing':'beep boop'})
        Traceback (most recent call last):
        ...
        YouNeedATokenForThat...
        >>> v.to_dict()['json']['json_other_thing']
        'blorg'

        Updating a thing with itself should be fine.
        >>> v.modify({'name':'Super Winery'})
        >>> v.modify({'json_other_thing':'blorg'})
        >>> v.modify({'location':location})

        You can update whatever you want if you have a stub.
        >>> v.modify({'location':other_location, 'token':'stub-uuid'})
        >>> v.subregion
        u'Similkameen Valley'

        Once a token has touched something it can still be changed.
        >>> v.modify({'completely_new_field':'hurfdorf'})

        """

        def field_edit_error(fieldname):
            return YouNeedATokenForThat(("You can't edit fields that already" +
                                          " exist: %s" % fieldname))
        can_edit_fields = False
        if 'token' in post:
            can_edit_fields = self.verify(post['token'])
            del post['token']

        if 'name' in post and post['name'] != self.to_dict()['name']:
            if not can_edit_fields:
                raise field_edit_error('name')
            else:
                self.name = post['name']
            del post['name']

        # if new location == old location, fugeddaboutit
        if ('location' in post and self.has_location and
            post['location'] == self.to_dict()['location'] ):
            del post['location']

        if 'location' in post:
            location = post['location']
            # a proper location can trump a location_fuzzy
            if (not self.has_location and self.has_location_fuzzy
                    and location in regions.location_list):
                self.set_location(location)
                self.location_fuzzy = None
            # a more specific location can trump a less specific location
            # something trumps nothing
            elif (not self.has_location and not self.has_location_fuzzy):
                self.set_location(location)
            elif can_edit_fields:
                self.set_location(location)
            else:
                raise field_edit_error('location')
            del post['location']

        json = BaseModel.tidy_up_the_post_object(post)

        if self.has_json:
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

        self.put()

    def verify(self, token=None):
        """
        If the token doesn't exist, return False
        If the token exists and belongs to the winery, return "True",
            and set self.verified and self.verified_by
        If the token exists and belongs to a verifier, return "True",
            and set self.verified and self.verified_by
        If the token exists but doesn't belong, return False

        >>> v = Winery()
        >>> v.create({'name':'Winery'})
        <stubs.Key object...>
        >>> v.private_token
        'stub-uuid'
        >>> v.verify('butts')
        False
        >>> v.has_verified
        False
        >>> v.verify('stub-uuid')
        True
        >>> v.verified_by
        'Winery'

        """
        if not token:
            return False
        if token == self.private_token:
            self.verified = True
            self.verified_by = "Winery"
            return True
        return False

    def update(self, wines=[]):
        """
        Recalculate this object's rank, 
        and
        create a search index for it. 
        """
        if not self.key:
            raise ArgumentException("Can't update without a key.")

        index = search.Index(name="wineries")
        
        searchkey = str(self.key.id())
        self.rank = self.calculate_rank(wines)
        
        location = ""
        if self.has_location:
            location = self.to_dict()['location']
        elif self.has_location_fuzzy:
            location = self.to_dict()['location_fuzzy']
        partial_location = BaseModel.partial_search_string(location)

        fields = []

        name = self.to_dict()['name']
        partial_name = BaseModel.partial_search_string(name)
        fields.append(search.TextField(name='name', value=name))
        fields.append(search.TextField(name='partial_name', 
                                       value=partial_name))

        fields.append(search.TextField(name='location', value=location))
        fields.append(search.TextField(name='partial_location', 
                                       value=partial_location))
        
        if self.has_country:
            country = self.to_dict()['country']
            fields.append(search.AtomField(name='country', value=country))

        if self.has_region:
            region = self.to_dict()['region']
            fields.append(search.AtomField(name='region', value=region))

        if self.has_subregion:
            region = self.to_dict()['subregion']
            fields.append(search.AtomField(name='subregion', value=subregion))

        fields.append(search.AtomField(name='verified', 
                                       value=str(self.has_verified)))

        fields.append(search.NumberField(name='rank', 
                                         value=self.rank))
        
        fields.append(search.TextField(name='id', 
                                       value=str(self.key.id())))

        searchdoc = search.Document(doc_id = searchkey,
                                    fields=fields,
                                    rank=self.rank) 
        
        index.put(searchdoc)
        return None

    def calculate_rank(self, wines=[]):
        """
        A potentially expensive operation, to try to quantify
        how much data this Winery object contains.
        More is better.
        """
        rank = 0
        if self.has_verified and self.has_verified_by:
            rank += 10000
        if self.has_country:
            rank += 50
        if self.has_region:
            rank += 100
        if self.has_subregion:
            rank += 200
        if not self.has_location and self.has_location_fuzzy:
            rank += 50

        if self.has_json:
            for key in self.to_dict()['json']:
                rank += 10

        for wine in wines:
            rank += wine.calculate_rank()

        return rank

    def to_dict(self):
        """
        Get the contents of this model as a dictionary.
        Never includes 'private_token'
        Tries to include 'key'
        """
        dict_ = copy.deepcopy(super(Winery, self).to_dict())
        if 'private_token' in dict_:
            del dict_['private_token']
        try:
            if self.key:
                dict_['key'] = self.key.id()
        except AttributeError:
            pass
        return dict_

    def set_location(self, location):
        """
        Given a location from the list of locations provided by
        regions.py (i.e. "Canada - British Columbia: Okanagan Valley")
        parse it into country, region, and subregion, and save
        those to the model.

        >>> v = Winery()
        >>> v.set_location("Canada - British Columbia: Okanagan Valley")
        >>> v.country
        u'Canada'
        >>> v.region
        u'British Columbia'
        >>> v.subregion
        u'Okanagan Valley'

        >>> v = Winery()
        >>> v.set_location("What is this I don't even")
        >>> v.country
        <stubs.StringProperty instance at ...>
        >>> v.location_fuzzy
        "What is this I don't even"

        """
        if location not in regions.location_list:
            self.location_fuzzy = location
        else:
            country, region, subregion = regions.location_map[location]
            self.location = location
            if country:
                self.country = country
            if region:
                self.region = region
            if subregion:
                self.subregion = subregion


    @staticmethod
    def country_query(country):
        qry = Winery.query(Winery.country == country)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.name,
                                            Winery.verified, Winery.location])
        return [x for x in results]

    @staticmethod
    def region_query(region):
        qry = Winery.query(Winery.region == region)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.name,
                                            Winery.verified, Winery.location])
        return [x for x in results]

    @staticmethod
    def subregion_query(subregion):
        qry = Winery.query(Winery.subregion == subregion)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.name,
                                            Winery.verified, Winery.location])
        return [x for x in results]

    @staticmethod
    def name_query(name):
        qry = Winery.query(Winery.name == name)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.verified,
                                                     Winery.location])
        return [x for x in results]

    @staticmethod
    def verified_query(verified):
        qry = Winery.query(Winery.verified == verified)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.name,
                                                     Winery.location])
        return [x for x in results]

    @staticmethod
    def verified_by_query(verified_by):
        qry = Winery.query(Winery.verified_by == verified_by)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.name,
                                                     Winery.location])
        return [x for x in results]

    @staticmethod
    def location_query(location):
        qry = Winery.query(Winery.location == location)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.name,
                                                     Winery.verified])
        return [x for x in results]

    @staticmethod
    def location_fuzzy_query(location):
        qry = Winery.query(Winery.location_fuzzy == location)
        results = qry.fetch(MAX_RESULTS, projection=[Winery.name,
                                                     Winery.verified])
        return [x for x in results]

    @staticmethod
    def all_fuzzy_locations():
        qry = Winery.query(Winery.location_fuzzy != None)
        results = qry.fetch(MAX_RESULTS)
        return [x.location_fuzzy for x in results]
