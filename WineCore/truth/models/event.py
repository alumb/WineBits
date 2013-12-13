from truth.models.base import BaseModel
from truth.stubs import ndb, uuid, search

actions = ["CREATE", "UPDATE"]
models = ["Winery", "Wine"]

class Event(BaseModel):
    """
    User <X> has created model <Key> at time <Z>
    """
    user = ndb.StringProperty(required=True, indexed=False)
    action = ndb.StringProperty(required=True, choices=actions)
    model = ndb.KeyProperty(required=True)
    model_type = ndb.StringProperty(required=True, choices=models)
    time = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create(user, model_type, model):
        e = Event()
        e.action = "CREATE"
        e.user = user
        e.model = model
        e.model_type = model_type
        return e.put()

    @staticmethod
    def update(user, model_type, model):
        e = Event()
        e.action = "UPDATE"
        e.user = user
        e.model = model
        e.model_type = model_type
        return e.put()

