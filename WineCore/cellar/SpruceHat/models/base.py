from cellar.SpruceHat.stubs import ndb
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
