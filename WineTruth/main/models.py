from slugify import slugify
import regions
import wine_types

import uuid

from google.appengine.ext import ndb

class VerifiedToken(ndb.Model):
    name = ndb.StringProperty(required=True)
    token = ndb.StringProperty(required=True)

class PostError(Exception):
    pass

class Vintner(ndb.Model):
    name = ndb.StringProperty(required=True)
    slug = ndb.ComputedProperty(lambda self: self.autoslug())
    verified = ndb.KeyProperty(kind=VerifiedToken)

    country = ndb.StringProperty(choices=regions.countries)
    region = ndb.StringProperty(choices=regions.regions)
    subregion = ndb.StringProperty(choices=regions.subregions)

    location = ndb.ComputedProperty(lambda self: self.get_location())
    location_fuzzy = ndb.StringProperty(indexed=False)

    addresses = ndb.TextProperty(repeated=True, indexed=False)
    geopts = ndb.GeoPtProperty(repeated=True)

    website = ndb.StringProperty()

    def create(self, post):
        if not 'name' in post:
            raise PostError("'name' field is mandatory")
        self.name = post['name']

        if 'location' in post:
            location = post['location']
            if location not in regions.location_list:
                self.location_fuzzy = location
            else:
                self.set_location(location)

        if 'address' in post:
            addresses = json.loads(post['addresses'])
            if type(addresses) != list:
                raise PostError("'addresses' field must be a JSON list.")
            self.addresses = addresses

        if 'geopts' in post:
            geopts = json.loads(post['geopts'])
            if type(geopts) != list:
                raise PostError("'geopts' field must be a JSON list.")
            try:
                geopts = [ndb.GeoPt(x['lat'], x['long']) for x in geopts]
            except KeyError:
                raise PostError("'geopt' object must contain 'lat' and 'long' fields.")
            self.geopts = geopts

        if 'website' in post:
            self.website = post['website']

        self.put()
        return self.put()

    def set_location(self, location):
        country, region, subregion = regions.location_map[location]
        if country:
            self.country = country
        if region:
            self.region = region
        if subregion:
            self.subregion = subregion

    def get_location(self):
        return regions.format_region(self.country, self.region, self.subregion)

    def autoslug(self):
        return slugify(self.name)

class Wine(ndb.Model):
    # Parent: Vintner
    year = ndb.StringProperty()
    slug = ndb.ComputedProperty(lambda self: self.autoslug())
    name = ndb.StringProperty()
    winetype = ndb.StringProperty(required=True, choices=wine_types.types)
    varietal = ndb.StringProperty()
    upc = ndb.StringProperty()
    verified = ndb.KeyProperty(kind=VerifiedToken)
    json = ndb.JsonProperty()

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
