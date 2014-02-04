from truth.models.base import BaseModel
from truth.constants import MAX_RESULTS
from truth.stubs import ndb, search
import json

class UserWine(BaseModel):
    user = ndb.UserProperty()
    drink_after = ndb.DateProperty()
    drink_before = ndb.DateProperty()
    tags = ndb.StringProperty(repeated=True) # list of tags

    def config(self, data):
        self.apply(["drink_before","drink_after"],data)
        if 'user_id' in data:
            self['user'] = data['user_id']
            del data['user_id']

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


