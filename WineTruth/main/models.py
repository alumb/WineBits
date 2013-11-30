from slugify import slugify
import regions
import wine_types

import os
import copy

from stubs import ndb, uuid, debug

if debug:
    MAX_RESULTS = 100
else:
    MAX_RESULTS = 5000

class VerifiedToken(ndb.Model):
    name = ndb.StringProperty(required=True)
    token = ndb.StringProperty(required=True)

    @staticmethod
    def authenticate(token):
        if debug and token == 'stub-token':
            return "stub-user"


class YouNeedATokenForThat(Exception):
    pass


def tidy_up_the_post_object(post):
    post = add_json_fields_to_the_post_object(post)
    post = remove_reserved_fields_from_the_post_object(post)
    return post


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
    return post


class Vintner(ndb.Model):
    """
    Represents a single wine producer.
    """
    name = ndb.StringProperty(required=True)

    location = ndb.StringProperty(choices=regions.location_list)
    location_fuzzy = ndb.StringProperty()

    def has_key(self, key):
        dict_ = self.to_dict()
        return key in dict_ and dict_[key] != "" and dict_[key] != {}

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
        Given a dict 'post' object containing vintner-y fields,
        populate and put this Vintner object, return the key.

        Throws a ValueError if no 'name' is included.
        >>> v_for_vintner = Vintner()
        >>> v_for_vintner.create({})
        Traceback (most recent call last):
        ...
        ValueError: 'name' field is mandatory

        Basic use-case test.
        >>> location = 'Canada - British Columbia: Okanagan Valley'
        >>> post = {'name':'Super Winery', 'location':location }
        >>> v_for_vintner = Vintner()
        >>> database_key = v_for_vintner.create(post)
        >>> v_for_vintner.country
        u'Canada'
        >>> v_for_vintner.region
        u'British Columbia'
        >>> v_for_vintner.subregion
        u'Okanagan Valley'
        >>> database_key
        'stub-key'

        If the location isn't in our list, it goes into location_fuzzy
        >>> location = 'Other'
        >>> post = {'name':'Super Winery 2', 'location':location}
        >>> v_for_vintner = Vintner()
        >>> database_key = v_for_vintner.create(post)
        >>> v_for_vintner.to_dict()
        {'location_fuzzy': 'Other', ...}
        >>> v_for_vintner.to_dict()['location_fuzzy']
        'Other'

        Vintners get a private token, which doesn't appear in to_dict()
        >>> v_for_vintner.private_token
        'stub-uuid'
        >>> v_for_vintner.to_dict()['private_token']
        Traceback (most recent call last):
        ...
        KeyError: 'private_token'

        Fields that we don't have database rows for go into the JSON.
        >>> post = {'name':'Super Winery 3', 'other_field':'glerg'}
        >>> v_for_vintner = Vintner()
        >>> database_key = v_for_vintner.create(post)
        >>> v_for_vintner.json
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

        # special: vintners + verifieds are magic
        if 'token' in post:
            self.verify(post['token'])
            del post['token']

        # having taken care of 'name' and 'location',
        # we wedge everything else into the JSON
        json = tidy_up_the_post_object(post)
        self.json = json

        key = self.put()
        return key

    def update(self, post):
        """
        Given a dict 'post' object containing vintner-y fields,
        update this object.

        Empty fields can always be updated. Fields cannot be overwritten
        without a valid vintner or verifier token.

        If this object has been verified, no changes may occur without
        a valid vintner or verifier token.

        Throws a YouNeedATokenForThat error if the user tries something
        he doesn't have access to without a token

        Let's create a Vintner to update...
        >>> location = 'Canada - British Columbia: Okanagan Valley'
        >>> post = {'name':'Super Winery' }
        >>> post['location_fuzzy'] = 'Somewhere'
        >>> post['json_thing'] = 'blerg'
        >>> v = Vintner()
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

        Once a token has touched something it can never be changed again.
        >>> v.update({'completely_new_field':'hurfdorf'})
        Traceback (most recent call last):
        ...
        YouNeedATokenForThat...
        """

        def field_edit_error(fieldname):
            return YouNeedATokenForThat(("You can't edit fields that already" +
                                          " exist: %s" % fieldname))
        can_edit_fields = False
        if 'token' in post:
            can_edit_fields = self.verify(post['token'])
            del post['token']

        # Once verified, it can never be changed again
        if (self.has_verified and self.to_dict()['verified']
            and not can_edit_fields):
            raise YouNeedATokenForThat("You can't edit verified records.")

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

    def verify(self, token=None):
        """
        If the token doesn't exist, return False
        If the token exists and belongs to the vintner, return "True",
            and set self.verified and self.verified_by
        If the token exists and belongs to a verifier, return "True",
            and set self.verified and self.verified_by
        If the token exists but doesn't belong, return False

        >>> v = Vintner()
        >>> v.create({'name':'Winery'})
        'stub-key'
        >>> v.private_token
        'stub-uuid'
        >>> v.verify('butts')
        False
        >>> v.has_verified
        False
        >>> v.verify('stub-uuid')
        True
        >>> v.verified_by
        'Vintner'
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
            self.verified_by = "Vintner"
            return True
        else:
            user = VerifiedToken.authenticate(token)
            if user:
                self.verified = True
                self.verified_by = user
                return True
        return False

    def to_dict(self):
        """
        Get the contents of this model as a dictionary.
        Never includes 'private_token'
        Tries to include 'key'
        """
        dict_ = copy.deepcopy(super(Vintner, self).to_dict())
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

        >>> v = Vintner()
        >>> v.set_location("Canada - British Columbia: Okanagan Valley")
        >>> v.country
        u'Canada'
        >>> v.region
        u'British Columbia'
        >>> v.subregion
        u'Okanagan Valley'

        >>> v = Vintner()
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
        qry = Vintner.query(Vintner.country == country)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.name,
                                            Vintner.verified, Vintner.location])
        return [x for x in results]

    @staticmethod
    def region_query(region):
        qry = Vintner.query(Vintner.region == region)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.name,
                                            Vintner.verified, Vintner.location])
        return [x for x in results]

    @staticmethod
    def subregion_query(subregion):
        qry = Vintner.query(Vintner.subregion == subregion)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.name,
                                            Vintner.verified, Vintner.location])
        return [x for x in results]

    @staticmethod
    def name_query(name):
        qry = Vintner.query(Vintner.name == name)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.verified,
                                                     Vintner.location])
        return [x for x in results]

    @staticmethod
    def verified_query(verified):
        qry = Vintner.query(Vintner.verified == verified)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.name,
                                                     Vintner.location])
        return [x for x in results]

    @staticmethod
    def verified_by_query(verified_by):
        qry = Vintner.query(Vintner.verified_by == verified_by)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.name,
                                                     Vintner.location])
        return [x for x in results]

    @staticmethod
    def location_query(location):
        qry = Vintner.query(Vintner.location == location)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.name,
                                                     Vintner.verified])
        return [x for x in results]

    @staticmethod
    def location_fuzzy_query(location):
        qry = Vintner.query(Vintner.location_fuzzy == location)
        results = qry.fetch(MAX_RESULTS, projection=[Vintner.name,
                                                     Vintner.verified])
        return [x for x in results]

    @staticmethod
    def all_fuzzy_locations():
        qry = Vintner.query(Vintner.location_fuzzy != None)
        results = qry.fetch(MAX_RESULTS)
        return [x.location_fuzzy for x in results]



class Place(ndb.Model):
    address = ndb.TextProperty(indexed=False)
    geopt = ndb.TextProperty(indexed=False)


class Wine(ndb.Model):
    # Parent: Vintner
    year = ndb.StringProperty()
    slug = ndb.ComputedProperty(lambda self: self.autoslug())
    name = ndb.StringProperty()
    winetype = ndb.StringProperty(required=True, choices=wine_types.types)
    varietal = ndb.StringProperty()
    upc = ndb.StringProperty()
    verified = ndb.KeyProperty(kind=VerifiedToken)
    json = ndb.JsonProperty(indexed=False)
    # JSON properties encompass the bits that might want to be tracked
    # but are too fiddly to keep track of regularly, like
    # bud_break, veraison, oak_regime, barrel_age, harvest_date,
    # bottling_date, alcohol_content, winemaker_notes, vineyard_notes...

    def autoslug(self):
        if self.year and self.name:
            return slugify(self.year + "-" + self.name)
        elif self.year and self.varietal:
            return slugify(self.year + "-" + self.varietal)
        elif self.name:
            return slugify(self.name)
        elif self.varietal:
            return slugify(self.varietal)
        else:
            return slugify(self.winetype)
