from truth.models.wine import Wine
from truth.models.winery import Winery
from truth.stubs import debug
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


def model_to_json(model):
    """
    Converts Models into dicts
    >>> v = Winery()
    >>> key = v.create({'name':'Winery'})
    >>> MyHandler.json(v)
    {...'name': 'Winery'...}

    Adds Model links
    >>> MyHandler.json(v)
    {...'url': '/winery/stub-key'...}

    Flattens json elements
    >>> MyHandler.json({'json':{'thing':'awesome'}})
    {...'thing': 'awesome'...}
    """
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
        return object_
    except AttributeError as e:
        return model


def json_response(handler, model):
    """
    Return object_ as JSON, with 'application/json' type.
    Strip out any 'json' field

    """
    if type(model) != list:
        object_ = model_to_json(model)
    else:
        object_ = [model_to_json(o) for o in model]

    handler.response.content_type="application/json"
    if debug:
        handler.response.write( json.dumps(object_, indent=2 ))
    else:
        handler.response.write( json.dumps(object_) )

