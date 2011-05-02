from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('blackjack.views',
    (r'^tables', 'table_list'),
    (r'^table/?$', 'table'),                       
    (r'', direct_to_template, {'template': 'blackjack/table/table.html'},)
)
