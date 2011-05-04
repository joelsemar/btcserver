""" WebSocket test resource.

This code will run a websocket resource on 8080 and reachable at ws://localhost:8080/test.
For compatibility with web-socket-js (a fallback to Flash for browsers that do not yet support
WebSockets) a policy server will also start on port 843.
See: http://github.com/gimite/web-socket-js
"""

__author__ = 'Reza Lotun'


from datetime import datetime
import simplejson
from collections import defaultdict
from twisted.internet.protocol import Protocol, Factory
from twisted.web import server, xmlrpc
from twisted.web.static import File
from twisted.internet import task
from webservice_tools.twisted.websocket import WebSocketHandler, WebSocketSite
from twisted.internet import reactor, protocol
from twisted.protocols.memcache import MemCacheProtocol, DEFAULT_PORT



class ClientConnectionManager(xmlrpc.XMLRPC):
    """
    Manages client connections
    Respond to xmlrpc updates from the django side, pass along through websocket to game client,
    provide some functionality for
    targeting tables and specific users on a table.
    """
    isLeaf = True
    
    
    def __init__(self, *args, **kwargs):
        self.registered_handlers = defaultdict(list)
        self.KEY_FORMAT = "TABLE_ID_%s"
        self._cached_game_state = None
        xmlrpc.XMLRPC.__init__(self, *args, **kwargs)
        
    
    def xmlrpc_update_table(self, response):
        if response.get('action') == 'update_game':
            self._cached_game_state = response
        table_id = response.get('table_id')
        game_handlers = self.registered_handlers[self.KEY_FORMAT % table_id]
        for handler in game_handlers:        
            handler.send(response)
    
    def xmlrpc_update_user(self, response):
        table_id = response.get('table_id')
        player_id = response.get('player_id')
        assert player_id
        game_handlers = self.registered_handlers.get(self.KEY_FORMAT % table_id)
        game_handlers = [g for g in game_handlers if g.player_id == player_id]
        for handler in game_handlers:        
            handler.send(response)
    
    
    def register(self, handler):
        key = self.KEY_FORMAT % handler.table_id
        handlers = self.registered_handlers[key]
        if handler not in handlers:
            handlers.append(handler)
        if self._cached_game_state:
            payload = self._cached_game_state
            payload['player_id'] = handler.player_id
            handler.send(payload)

    def deregister(self, handler):
        key = self.KEY_FORMAT % handler.table_id
        handlers = self.registered_handlers[key]
        if handler  in handlers:
            handlers.remove(handler)


class ClientHandler(WebSocketHandler):
    def __init__(self, transport):
        WebSocketHandler.__init__(self, transport)

    def __del__(self):
        print 'Deleting handler'    
    
    def register(self):
        global client_connection_manager
        client_connection_manager.register(self)
    
    def send(self, data):
        print 'Sending: %s to %s' % (data, self.player_id)
        self.transport.write(simplejson.dumps(data))

    def frameReceived(self, frame):
        try:
            data = simplejson.loads(frame)
        except:
            print frame
            
        table_id = data.get('table_id')
        player_id = data.get('player_id')
        if table_id and player_id:
            self.table_id = table_id
            self.player_id = player_id
            self.register()
            self.transport.write(simplejson.dumps(dict(registration_success=True)))
            
        #print 'Peer: ', self.transport.getPeer()

    def connectionMade(self):
        print 'Connected to client.'
        print 'Peer: ', self.transport.getPeer()

    def connectionLost(self, reason):
        global client_connection_manager
        client_connection_manager.deregister(self)
        print 'Lost connection.'
        # here is a good place to deregister this handler object


class FlashSocketPolicy(Protocol):
    """ A simple Flash socket policy server.
    See: http://www.adobe.com/devnet/flashplayer/articles/socket_policy_files.html
    """
    def connectionMade(self):
        policy = '<?xml version="1.0"?><!DOCTYPE cross-domain-policy SYSTEM ' \
                 '"http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">' \
                 '<cross-domain-policy><allow-access-from domain="*" to-ports="*" /></cross-domain-policy>'
        self.transport.write(policy)
        self.transport.loseConnection()

import os
from twisted.application import service, internet
from twisted.web import static, server

def getSocketService():
    """
    Return a service suitable for creating an application object.

    This service is a simple web server that serves files on port 8080 from
    underneath the current working directory.
    """
    # create a resource to serve static files
    root = server.Site(File('.'))
    site = WebSocketSite(root)
    site.addHandler('/test', ClientHandler)
    return internet.TCPServer(8080, site)


def getFlashPolicy():
    factory = Factory()
    factory.protocol = FlashSocketPolicy
    return internet.TCPServer(843, factory)


def getClientConnectionService():
    global client_connection_manager
    xmlrpc.addIntrospection(client_connection_manager)
    site = server.Site(client_connection_manager)
    return internet.TCPServer(9090, site)

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Demo application")

# attach the service to its parent application
ws_service = getSocketService()
ws_service.setServiceParent(application)

flash_service = getFlashPolicy()
flash_service.setServiceParent(application)

client_connection_manager = ClientConnectionManager(allowNone=True)
client_connection_service = getClientConnectionService()
client_connection_service.setServiceParent(application)
