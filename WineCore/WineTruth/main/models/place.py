from stubs import ndb

class Place(ndb.Model):
    # Parent: Winery
    address = ndb.TextProperty(indexed=False)
    geopt = ndb.TextProperty(indexed=False)
