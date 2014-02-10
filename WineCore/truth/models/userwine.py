from truth.models.base import BaseModel
from truth.stubs import ndb
import json

class UserWine(BaseModel):
    user = ndb.KeyProperty()
    drink_after = ndb.DateProperty()
    drink_before = ndb.DateProperty()
    tags = ndb.StringProperty(repeated=True) # list of tags

    def config(self, data):
        self.apply(["drink_before","drink_after"],data)
        if 'user' in data:
            self.user = data['user'].key
            del data['user']

        if 'tags' in data:
            tags = json.loads(data['tags'])
            if type(tags) != list:
                tags = [tags]
            self.tags = list(set(self.tags + tags)) 
            del data['tags']

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


