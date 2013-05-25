import urllib
import urllib2
import simplejson
import sys
import types
import logging
from datetime import datetime
from services.response import JSONResponse
from django.db import transaction
from django.contrib.gis.geos import fromstr
GOOGLE_REVERSE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false'
GOOGLE_API_URL = "http://maps.google.com/maps/geo?output=json&sensor=false"
        
class ReverseGeoCode():      

    def __init__(self, latlng):
        self.query = friendly_url_encode({'latlng': latlng})
    

    def get_address(self):
        response = simplejson.loads(urllib2.urlopen(GOOGLE_REVERSE_URL + '&' + self.query).read())
        ret = response['results']
        if not ret:
            raise GeoCodeError('Invalid coordinates')
        return ret
            
            
class GeoCode():
    
    def __init__(self, address):
        self.query = friendly_url_encode({'q': address})
    
    def _make_call(self):
        return simplejson.loads(urllib2.urlopen(GOOGLE_API_URL + '&' + self.query).read())
    
    def get_response(self):
        return  self._make_call()["Placemark"]
   
    def get_coords(self):
        response = self._make_call()
        coordinates = response['Placemark'][0]['Point']['coordinates'][0:2]
        return tuple([float(n) for n in coordinates])
            
            
def friendly_url_encode(data):
    # makes sure that for every item in your data dictionary that is of unicode type, it is first UTF-8
    # encoded before passing it in to urllib.urlencode()
    data = dict([(k, v.encode('utf-8') if type(v) is types.UnicodeType else v) for (k, v) in data.items()])
    return urllib.urlencode(data)


def location_from_coords(lng, lat):
    return fromstr('POINT(%.5f %.5f)' % (float(lng), float(lat)))

def generic_exception_handler(request, exception):
    response = JSONResponse()
    _, _, tb = sys.exc_info()
    # we just want the last frame, (the one the exception was thrown from)
    lastframe = get_traceback_frames(tb)[-1]
    location = "%s in %s, line: %s" % (lastframe['filename'], lastframe['function'], lastframe['lineno'])
    response.add_errors([exception.message, location])
    logger = logging.getLogger('webservice')
    logger.debug([exception.message, location])
    if transaction.is_dirty():
        transaction.rollback()
    return response.send()


def get_traceback_frames(tb):
    """
    Coax the line number, function data out of the traceback we got from the exc_info() call
    """
    frames = []
    while tb is not None:
        # support for __traceback_hide__ which is used by a few libraries
        # to hide internal frames.
        
        if not tb.tb_frame.f_locals.get('__traceback_hide__'):
            frames.append({
                'filename': tb.tb_frame.f_code.co_filename,
                'function': tb.tb_frame.f_code.co_name,
                'lineno': tb.tb_lineno,
            })
        tb = tb.tb_next

    return frames

def default_time_parse(time_string):
    """
    Expects times in the formats: "2011-12-25 18:22",  "2011-12-25 18:22:12",  "2011-12-25 18:22:12.241512", "2012-02-29"
    Returns None on error 
    """
    formats = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d")

    if not time_string or not isinstance(time_string, basestring):
        return None

    for fmt in formats:
        try:
            return datetime.strptime(time_string, fmt)
        except ValueError:
            pass
    return None

def today():
    """
    Returns a datetime object for today with hour/min zeroed out
    """
    today = datetime.utcnow()    
    return datetime(today.year, today.month, today.day)
    
def flatten(seq):
    """
    Flattens an array or tuple into a 1d list
    """
    
    ret = []
    def _flatten(seq):
        for i in seq:
            if isinstance(i, (list, tuple)):
                _flatten(i)
            else:
                ret.append(i)
        return ret
    
    if isinstance(seq, tuple):
        return tuple(_flatten(seq))
    
    return _flatten(seq)
