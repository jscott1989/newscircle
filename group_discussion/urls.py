from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from group_discussion import views

router = routers.DefaultRouter()
router.register(r'users', views.TopicUserViewSet, base_name="user")
router.register(r'comments', views.CommentViewSet, base_name="comment")
router.register(r'groups', views.GroupViewSet, base_name="group")

urlpatterns = patterns(
    '',
    url(r'^$', 'group_discussion.views.index', name='index'),
    url(r'^create_topic$', 'group_discussion.views.create_topic',
        name='create_topic'),
    url(r'^discussion/(?P<pk>\d+)/reply$', 'group_discussion.views.reply',
        name='reply'),
    url(r'^discussion/(?P<pk>\d+)', 'group_discussion.views.discussion',
        name='discussion'),
    url(r'^simple/(?P<pk>\d+)', 'group_discussion.views.simple_discussion',
        name='simple_discussion'),

    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),

    url(r'^(?P<pk>\d+)/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
)
