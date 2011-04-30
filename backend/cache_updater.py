"""
Django uses this to communicate with twisted, letting the ws handlers know when to update the client
"""
import xmlrpclib
URL = 'http://127.0.0.1:9090'

def send(data):
    rpc = xmlrpclib.ServerProxy(URL, allow_none=True)
    rpc.update(data)
    