from django.conf.urls.defaults import patterns, include, url
from webservice_tools.apps.user.handlers import LoginHandler 
from webservice_tools import urls as service_urls
from backend.handlers import  UserHandler, AccountWithdrawalHandler
from webservice_tools.utils import Resource
from blackjack import urls as blackjack_urls
from django.contrib import admin
admin.autodiscover()

basepatterns = patterns('',
    (r'^services/', include(service_urls)),
    (r'^user/?$', Resource(UserHandler)),
    (r'^login/?$', Resource(LoginHandler)),
    (r'^withdrawal/?$', Resource(AccountWithdrawalHandler)),
    (r'^blackjack/', include(blackjack_urls)), 
    
    # Examples:
    # url(r'^$', 'blackjack.views.home', name='home'),
    # url(r'^blackjack/', include('blackjack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
urlpatterns = patterns('',
    (r'^btcserver/', include(basepatterns)),
    (r'', include(basepatterns)),
)               