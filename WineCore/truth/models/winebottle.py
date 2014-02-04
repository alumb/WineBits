from truth.models.base import BaseModel
from truth.constants import MAX_RESULTS
from truth.stubs import ndb, search
from truth.models.wine import Wine
from datetime import datetime

class WineBottle(BaseModel):
    # Parent: wine
    wine = ndb.KeyProperty()
    bottle_size = ndb.StringProperty()
    purchase_date = ndb.DateProperty()
    purchase_location = ndb.StringProperty()
    storage_location1 = ndb.StringProperty()
    storage_location2 = ndb.StringProperty()
    cost = ndb.IntegerProperty() # Stored as number of cents
    consumed = ndb.BooleanProperty(default=False)
    consumed_date = ndb.DateProperty()

    json = ndb.JsonProperty(indexed=False)

    def config(self, data):
        purchase_date = None
        self.apply(['bottle_size','purchase_date','purchase_location','storage_location1','storage_location2','consumed','consumed_date'],data)

        if 'cost' in data and data['cost'] != '':
            self.cost = int(float(data['cost']) * 100)
            del data['cost']

        json = BaseModel.tidy_up_the_post_object(data)
        self.json = json

        key = self.put();
        return key

    def create(self, data):
        self.config(data)
        key = self.put()
        return key

    def modify(self, data):
        self.config(data)
        key = self.put()
        return key

    def delete(self):
        self.key.delete()

