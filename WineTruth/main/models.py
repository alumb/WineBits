from slugify import slugify
import regions
import wine_types

import os

from stubs import ndb, uuid

class VerifiedToken(ndb.Model):
    name = ndb.StringProperty(required=True)
    token = ndb.StringProperty(required=True)

class PostError(Exception):
    pass

class Vintner(ndb.Model):
    """
    Represents a single wine producer.
    """
    name = ndb.StringProperty(required=True)

    country = ndb.StringProperty(choices=regions.countries)
    region = ndb.StringProperty(choices=regions.regions)
    subregion = ndb.StringProperty(choices=regions.subregions)

    location = ndb.ComputedProperty(lambda self: self.get_location())
    location_fuzzy = ndb.StringProperty(indexed=False)

    #security stuff
    verified = ndb.KeyProperty(kind=VerifiedToken, indexed=False)
    private_token = ndb.StringProperty(indexed=False)

    json = ndb.JsonProperty(indexed=False)
    # website, phone_number

    def create(self, post):
        """
        Given a dict 'post' object containing vintner-y fields,
        populate and put this Vintner object, return the key.

        Throws a PostError if anything goes wrong.

        >>> v_for_vintner = Vintner()
        >>> v_for_vintner.create({})
        Traceback (most recent call last):
        ...
        PostError: 'name' field is mandatory

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

        >>> location = 'Other'
        >>> post = {'name':'Super Winery 2', 'location':location}
        >>> v_for_vintner = Vintner()
        >>> database_key = v_for_vintner.create(post)
        >>> vars(v_for_vintner)
        {'location_fuzzy': 'Other', ...}
        >>> v_for_vintner.private_token
        'stub-uuid'
        >>> v_for_vintner.to_dict()['location_fuzzy']
        'Other'
        >>> v_for_vintner.to_dict()['private_token']
        Traceback (most recent call last):
        ...
        KeyError: 'private_token'

        >>> post = {'name':'Super Winery 3', 'other_field':'glerg'}
        >>> v_for_vintner = Vintner()
        >>> database_key = v_for_vintner.create(post)
        >>> v_for_vintner.json
        {'other_field': 'glerg'}

        """
        # name of vintner
        if not 'name' in post:
            raise PostError("'name' field is mandatory")
        name = post['name']
        self.name = name
        del post['name']

        # location of vintner
        if 'location' in post:
            location = post['location']
            self.set_location(location)
            del post['location']

        # having taken care of 'name' and 'location',
        # we wedge everything else into the JSON
        self.json = post

        self.private_token = uuid.uuid4().hex

        key = self.put()
        return key

    def to_dict(self):
        dict_ = super(Vintner, self).to_dict()
        if 'private_token' in dict_:
            del dict_['private_token']
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
            if country:
                self.country = country
            if region:
                self.region = region
            if subregion:
                self.subregion = subregion

    def get_location(self):
        return regions.format_region(self.country, self.region, self.subregion)

class Location(ndb.Model):
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
