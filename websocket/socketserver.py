""" WebSocket test resource.

This code will run a websocket resource on 8080 and reachable at ws://localhost:8080/test.
For compatibility with web-socket-js (a fallback to Flash for browsers that do not yet support
WebSockets) a policy server will also start on port 843.
See: http://github.com/gimite/web-socket-js
"""

__author__ = 'Reza Lotun'


from datetime import datetime
import simplejson
from twisted.internet.protocol import Protocol, Factory
from twisted.web import server, xmlrpc
from twisted.web.static import File
from twisted.internet import task
from webservice_tools.twisted.websocket import WebSocketHandler, WebSocketSite
from twisted.internet import reactor, protocol
from twisted.protocols.memcache import MemCacheProtocol, DEFAULT_PORT

KEY_FORMAT = "TABLE_ID_%s"

class CacheUpdater(xmlrpc.XMLRPC):
    isLeaf = True
    def xmlrpc_update(self, response):
        game_handler = registered_handlers.get(KEY_FORMAT % response.get('table_id'))
        if game_handler:
            game_handler.send(response.get('data'))

registered_handlers = {}

class GameHandler(WebSocketHandler):
    def __init__(self, transport):
        WebSocketHandler.__init__(self, transport)
        #self.periodic_call = task.LoopingCall(self.get_game)

    def __del__(self):
        print 'Deleting handler'    
    
    def register(self):
        registered_handlers[KEY_FORMAT % self.table_id] = self
    
    def send(self, data):
        self.transport.write(data)

    def frameReceived(self, frame):
        try:
            data = simplejson.loads(frame)
        except:
            print frame
            
        table_id = data.get('table_id')
        if table_id:
            self.table_id = table_id
            self.register()
            self.transport.write(simplejson.dumps(dict(registered=True)))
        #print 'Peer: ', self.transport.getPeer()
        #self.periodic_call.start(0.5)

    def connectionMade(self):
        print 'Connected to client.'
        print 'Peer: ', self.transport.getPeer()

    def connectionLost(self, reason):
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
    site.addHandler('/test', GameHandler)
    return internet.TCPServer(8080, site)


def getFlashPolicy():
    factory = Factory()
    factory.protocol = FlashSocketPolicy
    return internet.TCPServer(843, factory)


def getCacheUpdater():
    r = CacheUpdater(allowNone=True)
    xmlrpc.addIntrospection(r)
    site = server.Site(r)
    return internet.TCPServer(9090, site)

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Demo application")

# attach the service to its parent application
ws_service = getSocketService()
ws_service.setServiceParent(application)

flash_service = getFlashPolicy()
flash_service.setServiceParent(application)

cache_updater = getCacheUpdater()
cache_updater.setServiceParent(application)