from truth.stubs import ndb
from datetime import datetime
import json


class YouNeedATokenForThat(Exception):
    pass


class BaseModel(ndb.Model):
    """
    Utility functions
    """
    def has_key(self, key):
        dict_ = self.to_dict()
        return (key in dict_ and dict_[key] and dict_[key] != ""
                and dict_[key] != {})

    def __contains__(self, key):
        return self.has_key(key)

    def apply(self, fields, data):
        for field in fields:
            if field in data:
                value = None
                field_type = type(getattr(type(self), field))
                if field_type == ndb.DateProperty:
                    value = datetime.strptime(data[field], '%Y/%m/%d')
                elif field_type == ndb.IntegerProperty:
                    value = int(data[field])
                elif field_type == ndb.BooleanProperty:
                    value = data[field].lower() == "true"
                else:
                    value = data[field]
                setattr(self, field, value)
                del data[field]

    @staticmethod
    def partial_search_string(string):
        """
        In order for GAE Search to do a partial text search on a string,
        you need to store it as a text document containing each possible
        partial text combo:

        >>> BaseModel.partial_search_string("hello")
        'h he hel hell hello'

        >>> BaseModel.partial_search_string("hello world")
        'h he hel hell hello w wo wor worl world'

        This clearly implies left-only partial text - i.e.
        "hell" will find "hello world" but "orl" will not.

        """
        chunks = []
        words = string.split(" ")
        for word in words:
            for i in range(1, len(word) + 1):
                chunks.append(word[0:i])
        return " ".join(chunks)

    @staticmethod
    def tidy_up_the_post_object(post):
        """
        Before the POST dict can be used, we want to remove any
            fields that might conflict with names we're using.
        If the POST object has a 'json' key, anything underneath that
            key is extracted and moved to the base object.
        If a key's value is a JSON string, it's parsed (if possible).
        """
        post = BaseModel._add_json_fields_to_the_post_object(post)
        post = BaseModel._remove_reserved_fields_from_the_post_object(post)
        new_post = {}
        for key, value in post.iteritems():
            try:
                new_post[key] = json.loads(value)
            except ValueError:
                new_post[key] = value
            except TypeError:
                new_post[key] = value
        return new_post

    @staticmethod
    def _add_json_fields_to_the_post_object(post):
        # Add JSON fields directly to the post object
        if 'json' in post:
            for key, value in post['json'].iteritems():
                post[key] = value
            del post['json']
        return post

    @staticmethod
    def _remove_reserved_fields_from_the_post_object(post):
        if 'name' in post:
            del post['name']
        if 'rank' in post:
            del post['rank']
        if 'country' in post:
            del post['country']
        if 'region' in post:
            del post['region']
        if 'subregion' in post:
            del post['subregion']
        if 'verified' in post:
            del post['verified']
        if 'verified_by' in post:
            del post['verified_by']
        if 'private_token' in post:
            del post['private_token']
        if 'token' in post:
            del post['token']
        if 'key' in post:
            del post['key']
        if 'link' in post:
            del post['link']
        if 'year' in post:
            del post['year']
        if 'winetype' in post:
            del post['winetype']
        if 'varietal' in post:
            del post['varietal']
        if 'upc' in post:
            del post['upc']
        if 'json' in post:
            del post['json']
        return post
