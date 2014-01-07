from cellar.SpruceHat.models.base import BaseModel
from cellar.SpruceHat.constants import MAX_RESULTS
from cellar.SpruceHat.stubs import ndb, search
from truth.models.wine import Wine

class WineBottle(BaseModel):
    # Parent: wine
    yearBought = ndb.IntegerProperty()
    drinkBefor = ndb.IntegerProperty()
    drunkOn = ndb.DateProperty()

    json = ndb.JsonProperty(indexed=False)

    def create(self, data):
        name = None
        if 'yearBought' in data:
            yearBought = int(data['yearBought'])
            self.yearBought = yearBought
            del data['yearBought']


        name = None
        if 'drinkBefor' in data:
            drinkBefor = int(data['drinkBefor'])
            self.drinkBefor = drinkBefor
            del data['drinkBefor']


        name = None
        if 'drunkOn' in data and data['drunkOn'] != '':
            drunkOn = data['drunkOn']
            self.drunkOn = drunkOn
            del data['drunkOn']

        json = BaseModel.tidy_up_the_post_object(data)
        self.json = json

        key = self.put();
        return key

    def delete(self):
        self.key.delete()

    def to_JSON(self):
        jsondict = self.to_dict()
        jsondict["wine"] = self.key.parent().get().to_dict()
        jsondict["wine"]["winery"] = self.key.parent().parent().get().to_dict()
        return jsondict
