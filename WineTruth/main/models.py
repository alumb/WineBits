import regions
import wine_types

import os
import copy
import json

from stubs import ndb, uuid, debug

#TODO: Wine index searches
#TODO: "Cache Invalidation" events
#TODO: prime the database with sample data


if debug:
    MAX_RESULTS = 100
else:
    MAX_RESULTS = 5000

UPDATE_BATCH_SIZE = 5

class VerifiedToken(ndb.Model):
    name = ndb.StringProperty(required=True)
    token = ndb.StringProperty(required=True)
    created_by = ndb.StringProperty(required=True, indexed=False)

    @staticmethod
    def classam():
        qry = VerifiedToken.query(VerifiedToken.name == 'classam')
        results = qry.fetch(1)
        if len(results) > 0:
            return results[0].token
        return False

    @staticmethod
    def new_token(name, created_by):
        v = VerifiedToken(name=name, token=uuid.uuid4().hex,
                            created_by=created_by)
        v.put()
        return v.token

    @staticmethod
    def authenticate(token):
        if debug and token == 'stub-token':
            return "stub-user"
        else:
            qry = VerifiedToken.query(VerifiedToken.token == token)
            results = qry.fetch(1, projection=[VerifiedToken.name])
            results = [x for x in results]
            if len(results) > 0:
                return results[0].name
            return False



class YouNeedATokenForThat(Exception):
    pass


def tidy_up_the_post_object(post):
    post = add_json_fields_to_the_post_object(post)
    post = remove_reserved_fields_from_the_post_object(post)
    new_post = {}
    for key, value in post.iteritems():
        try:
            new_post[key] = json.loads(value)
        except ValueError:
            new_post[key] = value
        except TypeError:
            new_post[key] = value
    return new_post


def add_json_fields_to_the_post_object(post):
    # Add JSON fields directly to the post object
    if 'json' in post:
        for key, value in post['json'].iteritems():
            post[key] = value
        del post['json']
    return post


def remove_reserved_fields_from_the_post_object(post):
    if 'name' in post:
        del post['name']
    if 'rank' in post:
        del post['rank']
    if 'country' in post:
        del post['country']
    if 'region' in post:
        del post['region']
    if 'subregion' in post:
        del post['subregion']
    if 'verified' in post:
        del post['verified']
    if 'verified_by' in post:
        del post['verified_by']
    if 'private_token' in post:
        del post['private_token']
    if 'token' in post:
        del post['token']
    if 'key' in post:
        del post['key']
    if 'link' in post:
        del post['link']
    if 'year' in post:
        del post['year']
    if 'winetype' in post:
        del post['winetype']
    if 'varietal' in post:
        del post['varietal']
    if 'upc' in post:
        del post['upc']
    if 'json' in post:
        del post['json']
    return post


class MyModel(ndb.Model):
    """
    Utility functions
    """
    def has_key(self, key):
        dict_ = self.to_dict()
        return (key in dict_ and dict_[key] and dict_[key] != ""
                and dict_[key] != {})


class Winery(MyModel):
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
        json = tidy_up_the_post_object(post)
        self.json = json

        self.rank = self.calculate_rank()

        key = self.put()
        return key

    def update(self, post):
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
        >>> v.update(new_post)
        >>> v.country
        u'Canada'
        >>> v.to_dict()['json']['json_other_thing']
        'blorg'

        Updates of existing fields should fail.
        >>> other_location = 'Canada - British Columbia: Similkameen Valley'
        >>> v.update({'location':other_location})
        Traceback (most recent call last):
        ...
        YouNeedATokenForThat...

        Updates of json fields that already exist should fail.
        >>> v.update({'json_other_thing':'beep boop'})
        Traceback (most recent call last):
        ...
        YouNeedATokenForThat...
        >>> v.to_dict()['json']['json_other_thing']
        'blorg'

        Updating a thing with itself should be fine.
        >>> v.update({'name':'Super Winery'})
        >>> v.update({'json_other_thing':'blorg'})
        >>> v.update({'location':location})

        You can update whatever you want if you have a stub.
        >>> v.update({'location':other_location, 'token':'stub-uuid'})
        >>> v.subregion
        u'Similkameen Valley'

        Once a token has touched something it can still be changed.
        >>> v.update({'completely_new_field':'hurfdorf'})

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

        json = tidy_up_the_post_object(post)

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
        self.queued_update()

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
        >>> v.verify('stub-token')
        True
        >>> v.verified
        True
        >>> v.verified_by
        'stub-user'

        """
        if not token:
            return False
        if token == self.private_token:
            self.verified = True
            self.verified_by = "Winery"
            return True
        else:
            user = VerifiedToken.authenticate(token)
            if user:
                self.verified = True
                self.verified_by = user
                return True
        return False

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

    def queued_update(self):
        """
        If a winery is updated, it triggers potentially expensive operations
        that are queued for later. They go in here.
        As of right now, they just happen after
        a Winery or Wine update, but we're moving them to a task queue, 
        I promise. 
        """

        wines = self.wine_query()
        self.rank = self.calculate_rank(wines)
        self.put()
        #TODO: move queued_update to a task queue

        #TODO: update search index for winery and all wines here.



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

    def wine_query(self):
        qry = Wine.query(ancestor=self.key)
        results = qry.fetch(MAX_RESULTS)
        return [x for x in results]


class Wine(MyModel):
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

        json = tidy_up_the_post_object(post)
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

        json = tidy_up_the_post_object(post)
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
        winery.queued_update()
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
        else:
            user = VerifiedToken.authenticate(token)
            if user:
                self.verified = True
                self.verified_by = user
                return True
        return False


class Place(ndb.Model):
    # Parent: Winery
    address = ndb.TextProperty(indexed=False)
    geopt = ndb.TextProperty(indexed=False)
