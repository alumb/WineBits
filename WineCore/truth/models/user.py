from truth.models.base import BaseModel
from truth.stubs import ndb, users

import logging


class User(BaseModel):
    name = ndb.StringProperty()
    guser = ndb.UserProperty()
    email = ndb.StringProperty()
    cellar = ndb.KeyProperty()

    def create(self, data):
        logging.info("adding: " + data['email'])
        self.apply(['name', 'email', 'guser'], data)
        key = self.put()
        return key

    def delete(self):
        self.key.delete()

    @staticmethod
    def get_current_user():
        guser = users.get_current_user()
        if guser is None:
            raise Exception("Not Authenticated")
        qry = User.query(User.guser == guser)
        results = qry.fetch(1)
        if len(results) <= 0:  # create the user
            user = User()
            user.create({
                'guser': guser,
                'name': guser.nickname(),
                'email': guser.email()
            })
            return user
        else:
            return results[0]

    @staticmethod
    def has_access(cellar_key):
        return User.get_current_user().cellar == cellar_key
