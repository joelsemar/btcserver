from django.core import serializers
import simplejson
from django import dispatch
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.http import HttpResponse
##from services.emitters import JSONEmitter
from django.conf import settings

JSON_INDENT = 4 if settings.DEBUG else 0

JSONSerializer = serializers.get_serializer('json')

message_sent = dispatch.Signal(providing_args=['message'])

class BaseView(object):
    """
    A generic response object for generating and returning api responses
    """
    def __init__(self, request=None):
        self._errors = []
        self._request = request
        self._messages = []
        self.success = True
        self._data = {}
        self._status = 200
        self.doc = None
        self.headers = {}
        
        if self._request:
            message_sent.connect(self.message_callback, sender=None, dispatch_uid='response_receiver')
    
    def set_headers(self, headers):
        for k, v in headers.items():
            self.headers[k] = v
    
    
    def add_errors(self, errors, status=400):
        
        self.success = False
        
        if status:
            self._status = status
            
        if isinstance(errors, basestring):
            #just a single error
            self._errors.append(errors)
            return
        
        elif isinstance(errors, list):
            # a list of errors
            for error in errors:
                self._errors.append(error)
            return
        raise TypeError("Argument 'errors' must be of type 'string' or 'list'")
    
    
    def message_callback(self, signal, sender, **kwargs):
        message = kwargs.get('message', '')
        if self._request.user.id == sender.id:
            self.add_messages(message)
        
    
    def add_messages(self, messages):
        if isinstance(messages, basestring):
            #just a single message
            self._messages.append(messages)
            return
        
        elif isinstance(messages, (list, tuple)):
            # a list of errors
            for message in messages:
                self._messages.append(message)
            return
        self._messages.append(messages)

    
    def set(self, **kwargs):
        self._data.update(kwargs)
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __getitem__(self, key):
        return self._data[key]
        
    def get(self, key):
        return self._data[key]
    
    def setStatus(self, status):
        assert isinstance(status, int)
        self._status = status

    def render(self):
        return self._data
    

    def access_denied(self):
        return self.send("ACCESS DENIED", status=401)

    def bad_request(self):
        return self.send("BAD REQUEST", status=400)
    
    def send(self, messages=None, errors=None, status=None):
        
        if errors:
            self.add_errors(errors)
        
        if status:
            self.setStatus(status)
        
        if messages:
            self.add_messages(messages)
        
        response_dict = {}
        response_dict['data'] = self.render()
        response_dict['errors'] = self._errors
        response_dict['success'] = self.success

        if self._messages:
            response_dict['messages'] = messages

        if self.doc:
            response_dict['doc'] = self.doc
        
        response_body = simplejson.dumps(response_dict, cls=DateTimeAwareJSONEncoder, indent=JSON_INDENT)
        http_response = HttpResponse(response_body, status=self._status)
        http_response['Content-Type'] = 'application/json'
        return http_response

class ListView(BaseView):

    def render(self):
        ret = {}
        for key, value in self._data.items():
            if isinstance(value, (list, tuple)):
                ret[key] = [d.dict for d in value]
        return ret
