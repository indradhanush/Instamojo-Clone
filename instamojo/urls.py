from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instamojo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Clone related urls.
    url(r'^$', 'clone.views.index', name='index'),
    url(r'^register/', 'clone.views.register', name='register'),
    url(r'^login/', 'clone.views.login_user', name='login'),
    url(r'^logout/', 'clone.views.logout_user', name='logout'),
    url(r'^home/', 'clone.views.home', name='home')
)
