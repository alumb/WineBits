from cellar.SpruceHat.stubs import debug, webapp2
import json

class JsonView(webapp2.RequestHandler):
    @staticmethod
    def json(model):
        """

        """
        try:
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
            if id_:
                object_['id'] = id_
            return object_
        except AttributeError as e:
            return model

    @staticmethod
    def json_response(handler,  model):
        """
        Return object_ as JSON, with 'application/json' type.
        Strip out any 'json' field

        """
        if type(model) != list:
            object_ = JsonView.json(model)
        else:
            object_ = [JsonView.json(o) for o in model]

        handler.response.content_type="application/json"
        if debug:
            handler.response.write( json.dumps(object_, indent=2 ))
        else:
            handler.response.write( json.dumps(object_) )
