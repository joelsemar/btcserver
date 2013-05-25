
class InterfaceError(Exception):
    pass

def Implements(*interfaces):
    
    methods = [a for interface in interfaces for a in dir(interface) if not a.startswith('__')]
    def _implements(original_class):
        for method in methods:
            if method not in dir(original_class):
                raise InterfaceError("Class %s failed to implement %s" % (original_class, method))
        original_class.__implements__ = getattr(original_class, '__implements__', [])
        for interface in interfaces:
            original_class.__implements__.append(interface)
        return original_class
    return _implements


def implements(target, *args):
    if not hasattr(target, '__implements__'):
        return False
    
    for interface in args:
        if interface not in target.__implements__:
            return False
    return True
            


class ifaceFoo(object):
    def foo(self):
        "I foo and foo and till I can't foo no more"


class ifaceBar(object):
    
    age = 10
    def bar(self):
        "You want bars? I'm your fucking guy"

    
@Implements(ifaceBar, ifaceFoo)
class Bar(object):
    
    age = 11
    def bar(self):
        pass
    
    def foo(self):
        pass


def needs_a_bar(b):
    assert implements(b, ifaceBar)
    assert implements(b, ifaceFoo)    
