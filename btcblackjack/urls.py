from django.conf.urls.defaults import patterns, include, url
from webservice_tools.utils import Resource
from btcblackjack.handlers import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^tables/?$', Resource(BlackJackTablesHandler)),
    (r'^table/(?P<id>[\d]+', Resource(BlackJackTableHandler)),
    (r'^tabletypes/?$', Resource(BlackJackTableTypesHandler)),
)
