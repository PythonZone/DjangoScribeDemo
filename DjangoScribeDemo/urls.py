# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
# %JFE+[ added as an example of use for rest-framework
# see http://www.django-rest-framework.org/#example
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# %JFE+]

urlpatterns = patterns('',

    # %JFE+2 added to enable admindoc app
    # see https://docs.djangoproject.com/en/1.7/ref/contrib/admin/admindocs/#overview
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Examples:
    # url(r'^$', 'DjangoScribeDemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    # %JFE+2 added for django-select2
    # see https://github.com/applegrew/django-select2#installation
    url(r'^select2/', include('django_select2.urls')),
    # %JFE+3 added for rest-framework
    # see http://www.django-rest-framework.org/#installation
    url(r'^rest-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    # %JFE+2 added for rest-framework example. added at api here
    # see http://www.django-rest-framework.org/#example
    url(r'^rest/', include(router.urls)),
    # %JFE+2 added for rest-framework example. added at 'api' here
    # see http://www.django-rest-framework.org/#example
    url(r'^restdocs/', include('rest_framework_swagger.urls')),
    # %JFE+2 added for rest-framework example. added at 'sql/' here
    # see http://www.django-rest-framework.org/#example
    url(r'^sql/', include('explorer.urls')),
    # %JFE+2 added for django-silk
    # see https://github.com/mtford90/silk/#installation
    url(r'^silk/', include('silk.urls', namespace='silk')),
)
