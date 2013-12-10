from stubs import ndb
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



