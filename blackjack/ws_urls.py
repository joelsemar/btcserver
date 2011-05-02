from django.conf.urls.defaults import patterns, include, url
from webservice_tools.utils import Resource
from blackjack.handlers import *
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('blackjack.views',
    (r'^tables/?$', Resource(BlackJackTablesHandler)),
    (r'^table/(?P<id>[\d]+)/(?P<action>[\w]+)/?$', Resource(PlayerActionHandler)),
    (r'^table/(?P<id>[\d]+)/?$', Resource(BlackJackTableHandler)),
    (r'^tabletypes/?$', Resource(BlackJackTableTypesHandler)),
    (r'^cards/?$', Resource(CardsHandler)),
    
)
