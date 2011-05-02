"""
Django uses this to communicate with twisted, letting the ws handlers know when to update the client
"""
import xmlrpclib
URL = 'http://127.0.0.1:9090'


class ClientConnection(object):
        
    
    def __init__(self, data, table_id, action, user_id=None):
        self.rpc = xmlrpclib.ServerProxy(URL, allow_none=True)
        self.table_id = table_id
        self.user_id = user_id
        self.data = data
        self.action = action
        self.payload = self.new_payload()

    
    def new_payload(self):
        return {'action': self.action, 'data': self.data,
                'table_id': self.table_id, 'user_id': self.user_id}

    def send(self):
        if self.payload.get('user_id'):
            self.rpc.update_user(self.payload)
        else:
            self.rpc.update_table(self.payload)
            
    
