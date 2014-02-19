from truth.models.base import BaseModel
from truth.stubs import ndb


class WineCellar(BaseModel):
    name = ndb.StringProperty()

    def create(self, data):
        self.apply(["name"], data)
        key = self.put()
        return key

    def modify(self, data):
        self.apply(["name"], data)
        key = self.put()
        return key

    def delete(self):
        self.key.delete()
