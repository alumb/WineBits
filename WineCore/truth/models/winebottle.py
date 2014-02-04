from truth.models.base import BaseModel
from truth.constants import MAX_RESULTS
from truth.stubs import ndb, search
from truth.models.wine import Wine
from datetime import datetime

class WineBottle(BaseModel):
    # Parent: wine
    wine = ndb.KeyProperty()
    purchase_date = ndb.DateProperty()
    purchase_location = ndb.StringProperty()
    cost = ndb.IntegerProperty() # Stored as number of cents
    value = ndb.IntegerProperty() # values 1-5
    consumed = ndb.BooleanProperty()
    consumed_date = ndb.DateProperty()

    json = ndb.JsonProperty(indexed=False)

    def update(self, data):
        purchase_date = None
        if 'purchase_date' in data and data['purchase_date'] != '':
            purchase_date = datetime.strptime(data['purchase_date'], '%Y/%m/%d')
            self.purchase_date = purchase_date
            del data['purchase_date']

        purchase_location = None
        if 'purchase_location' in data and data['purchase_location'] != '':
            purchase_location = data['purchase_location']
            self.purchase_location = purchase_location
            del data['purchase_location']

        cost = None
        if 'cost' in data and data['cost'] != '':
            cost = int(float(data['cost']) * 100)
            self.cost = cost
            del data['cost']

        value = None
        if 'value' in data and data['value'] != '':
            value = int(data['value'])
            self.value = value
            del data['value']

        consumed = None
        if 'consumed' in data and data['consumed'] != '':
            consumed = data['consumed'] == "true" or data['consumed'] == "True"
            self.consumed = consumed
            del data['consumed']

        consumed_date = None
        if 'consumed_date' in data and data['consumed_date'] != '':
            consumed_date = datetime.strptime(data['consumed_date'], '%Y/%m/%d')
            self.consumed_date = consumed_date
            del data['consumed_date']

        json = BaseModel.tidy_up_the_post_object(data)
        self.json = json

        key = self.put();
        return key

    def delete(self):
        self.key.delete()

    def to_JSON(self):
        jsondict = self.to_dict()
        jsondict["id"] = self.key.id()
        jsondict["url"] = "/cellar/" + str(self.key.parent().id()) + "/wine/" + str(self.key.id())
        
        if "purchase_date" in jsondict and jsondict["purchase_date"] is not None:
            jsondict["purchase_date"] = jsondict["purchase_date"].strftime("%Y/%m/%d")

        if "consumed_date" in jsondict and jsondict["consumed_date"] is not None:
            jsondict["consumed_date"] = jsondict["consumed_date"].strftime("%Y/%m/%d")
        
        jsondict["wine"] = self.wine.get().to_dict()
        jsondict["wine"]["winery"] = self.wine.parent().get().to_dict()
        
        return jsondict
