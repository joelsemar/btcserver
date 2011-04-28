from django.conf.urls.defaults import patterns, include, url
from webservice_tools.apps.user import import urls as user_urls
from webservice_tools.apps.user.handlers import LoginHandler 
from webserice_tools import urls as service_urls
from btcserver.handlers import import UserHandler
from webservice_tools.utils import Resource
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^services/', include(service_urls)),
    url(r'^user/?$', Resource(UserHandler)),
    url(r'^login/?$', Resource(LoginHandler)),
    
    # Examples:
    # url(r'^$', 'btcblackjack.views.home', name='home'),
    # url(r'^btcblackjack/', include('btcblackjack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
