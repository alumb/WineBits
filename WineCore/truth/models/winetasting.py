from truth.models.base import BaseModel
from truth.stubs import ndb


class WineTasting(BaseModel):
    consumption_type = ndb.StringProperty()
    consumption_location = ndb.StringProperty()
    consumption_location_name = ndb.StringProperty()
    date = ndb.DateProperty()
    rating = ndb.IntegerProperty()
    flawed = ndb.BooleanProperty(default=False)
    note = ndb.StringProperty()

    def config(self, data):
        self.apply(["consumption_type", "consumption_location", "consumption_location_name",
                    "date", "rating", "flawed", "note"], data)

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
