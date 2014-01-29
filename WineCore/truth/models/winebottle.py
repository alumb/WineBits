from truth.models.base import BaseModel
from truth.constants import MAX_RESULTS
from truth.stubs import ndb, search
from truth.models.wine import Wine
from datetime import datetime

class WineBottle(BaseModel):
    # Parent: wine
    wine = ndb.KeyProperty()
    drinkAfter = ndb.DateProperty()
    drinkBefore = ndb.DateProperty()
    purchaseDate = ndb.DateProperty()
    purchaseLocation = ndb.StringProperty()
    cost = ndb.IntegerProperty() # Stored as number of cents
    value = ndb.IntegerProperty() # values 1-5
    consumed = ndb.BooleanProperty()
    consumedDate = ndb.DateProperty()

    json = ndb.JsonProperty(indexed=False)

    def update(self, data):
        drinkAfter = None
        if 'drinkAfter' in data:
            drinkAfter = datetime.strptime(data['drinkAfter'], '%Y/%m/%d')
            self.drinkAfter = drinkAfter
            del data['drinkAfter']

        drinkBefore = None
        if 'drinkBefore' in data:
            drinkBefore = datetime.strptime(data['drinkBefore'], '%Y/%m/%d')
            self.drinkBefore = drinkBefore
            del data['drinkBefore']

        purchaseDate = None
        if 'purchaseDate' in data and data['purchaseDate'] != '':
            purchaseDate = datetime.strptime(data['purchaseDate'], '%Y/%m/%d')
            self.purchaseDate = purchaseDate
            del data['purchaseDate']

        purchaseLocation = None
        if 'purchaseLocation' in data and data['purchaseLocation'] != '':
            purchaseLocation = data['purchaseLocation']
            self.purchaseLocation = purchaseLocation
            del data['purchaseLocation']

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

        consumedDate = None
        if 'consumedDate' in data and data['consumedDate'] != '':
            consumedDate = datetime.strptime(data['consumedDate'], '%Y/%m/%d')
            self.consumedDate = consumedDate
            del data['consumedDate']

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
        
        if "drinkAfter" in jsondict and jsondict["drinkAfter"] is not None:
            jsondict["drinkAfter"] = jsondict["drinkAfter"].strftime("%Y/%m/%d")

        if "drinkBefore" in jsondict and jsondict[ "drinkBefore"] is not None:
            jsondict["drinkBefore"] = jsondict["drinkBefore"].strftime("%Y/%m/%d")

        if "purchaseDate" in jsondict and jsondict["purchaseDate"] is not None:
            jsondict["purchaseDate"] = jsondict["purchaseDate"].strftime("%Y/%m/%d")

        if "consumedDate" in jsondict and jsondict["consumedDate"] is not None:
            jsondict["consumedDate"] = jsondict["consumedDate"].strftime("%Y/%m/%d")
        
        jsondict["wine"] = self.wine.get().to_dict()
        jsondict["wine"]["winery"] = self.wine.parent().get().to_dict()
        
        return jsondict
