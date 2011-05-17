from django.conf.urls.defaults import patterns, include, url
from webservice_tools.apps.user.handlers import LoginHandler 
from webservice_tools import urls as service_urls
from backend.handlers import  ChatHandler,UserHandler, AccountWithdrawalHandler
from webservice_tools.utils import Resource
from blackjack import web_urls as blackjack_web_urls, ws_urls as black_jack_ws_urls
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

web_patterns = patterns('',
    (r'^blackjack/', include(blackjack_web_urls)), 
    (r'^admin/', include(admin.site.urls)),
    (r'', direct_to_template, {'template': 'base.html'}),
)
ws_patterns = patterns('',
    (r'^services/', include(service_urls)),
    (r'^user/?$', Resource(UserHandler)),
    (r'^login/?$', Resource(LoginHandler)),
    (r'^withdrawal/?$', Resource(AccountWithdrawalHandler)),
    (r'^table/(?P<table_id>[\d]+)/chat/?$', Resource(ChatHandler)),
    (r'^blackjack/', include(black_jack_ws_urls)),
    
          
)

urlpatterns = patterns('',
    (r'^btcserver/', include(ws_patterns)),
    (r'', include(web_patterns)),
)               