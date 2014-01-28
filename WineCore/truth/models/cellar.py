from truth.models.base import BaseModel
from truth.constants import MAX_RESULTS
from truth.stubs import ndb, search

class WineCellar(BaseModel):
    name = ndb.StringProperty()

    def create(self, data):
        name = None
        if 'name' in data:
            name = data['name']
            self.name = name
            del data['name']

        key = self.put();
        return key

    def modify(self, data):
        name = None
        if 'name' in data:
            name = data['name']
            self.name = name
            del data['name']

        key = self.put();
        return key

    def delete(self):
        self.key.delete()


