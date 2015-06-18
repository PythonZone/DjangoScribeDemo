from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoScribeDemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # %JFE+2 added for django-select2
    # see https://github.com/applegrew/django-select2#installation
    url(r'^select2/', include('django_select2.urls')),
)
