from truth.models.base import BaseModel
from truth.stubs import ndb

actions = ["CREATE", "UPDATE"]

class Event(BaseModel):
    """
    User <X> has created model <Key> at time <Z>
    """
    user = ndb.StringProperty(required=True, indexed=False)
    action = ndb.StringProperty(required=True, choices=actions)
    model = ndb.KeyProperty(required=True)
    model_type = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def addEvent(event, user, model_type, model):
        e = Event()
        e.action = event
        e.user = user
        e.model = model
        e.model_type = model_type
        return e.put()

    @staticmethod
    def create(user, model_type, model):
        Event.addEvent("CREATE", user, model_type, model)
 
    @staticmethod
    def update(user, model_type, model):
        Event.addEvent("UPDATE", user, model_type, model)

    @staticmethod
    def delete(user, model_type, model):
        Event.addEvent("DELETE", user, model_type, model)

