from truth.models.wine import Wine
from truth.models.winery import Winery
from truth.stubs import debug, ndb
from datetime import date
from google.appengine.api import users
import json


def get_url(model):
    """
        >>> v = Winery()
        >>> key = v.create({'name':'Winery'})
        >>> get_url(v)
        '/winery/stub-key'

        >>> w = Wine(parent=key)
        >>> key = w.create({'winetype':'Red', 'year':'2010'}, v)
        >>> get_url(w)
        '/winery/stub-key/wine/stub-key'
    """
    if isinstance(model, Winery):
        return "/winery/%s" % str(model.key.id())
    if isinstance(model, Wine):
        parent_key = model.key.parent()
        return "/winery/%s/wine/%s" % (str(parent_key.id()), str(model.key.id()))
    return None


def model_to_json(model, extended_listing=False):

    try:
        url = get_url(model)
        try:
            id_ = model.key.id()
        except:
            id_ = None
        if not isinstance(model, dict):
            object_ = model.to_dict()
        else:
            object_ = model
        if object_ and 'json' in object_ and object_['json']:
            for key, value in object_['json'].iteritems():
                object_[key] = value
            del object_['json']
        if url:
            object_['url'] = url
        if id_:
            object_['id'] = id_
        for key, value in object_.iteritems():
            if issubclass(type(value), ndb.Key):
                if extended_listing:
                    object_[key] = model_to_json(value.get(), extended_listing)
                else:
                    object_[key] = value.id()
            if issubclass(type(value), date):
                object_[key] = value.strftime("%Y/%m/%d")
            elif issubclass(type(value), users.User):
                object_[key] = value.user_id()
            # else:
            #     logging.info(key + " -- " + str(type(value)))
        
        if extended_listing:
            parent = model.key.parent()
            while parent is not None:
                object_[parent.kind()] = model_to_json(parent.get(), extended_listing)
                parent = parent.parent()

        return object_
    except AttributeError:
        return model


def json_response(handler, model, extended_listing=False):
    """
    Return object_ as JSON, with 'application/json' type.
    Strip out any 'json' field

    """
    if type(model) != list:
        object_ = model_to_json(model, extended_listing)
    else:
        object_ = [model_to_json(o, extended_listing) for o in model]

    handler.response.content_type = "application/json"
    if debug:
        handler.response.write(json.dumps(object_, indent=2))
    else:
        handler.response.write(json.dumps(object_))
