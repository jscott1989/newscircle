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
    url(r'^info$', 'group_discussion.views.info',
        name='info'),
    url(r'^demographics$', 'group_discussion.views.demographics',
        name='demographics'),
    url(r'^create_topic$', 'group_discussion.views.create_topic',
        name='create_topic'),
    url(r'^discussion/(?P<pk>\d+)/pin', 'group_discussion.views.pin_topic',
        name='pin_topic'),
    url(r'^discussion/(?P<pk>\d+)/unpin', 'group_discussion.views.unpin_topic',
        name='unpin_topic'),
    url(r'^discussion/(?P<pk>\d+)/group/(?P<group>.+)/(?P<sort_by>.+)', 'group_discussion.views.view_group',
        name='view_group'),
    url(r'^discussion/(?P<pk>\d+)/reply$', 'group_discussion.views.reply',
        name='reply'),
    url(r'^discussion/(?P<pk>\d+)', 'group_discussion.views.discussion',
        name='discussion'),
    url(r'^user/(?P<pk>\d+)', 'group_discussion.views.profile',
        name='profile'),

    url(r'^consent', 'group_discussion.views.consent',
        name='consent'),
    url(r'^communicate', 'group_discussion.views.communicate',
        name='communicate'),

    url(r'^comments/(?P<pk>\d+)/like', 'group_discussion.views.like',
        name='like'),
    url(r'^comments/(?P<pk>\d+)/dislike', 'group_discussion.views.dislike',
        name='dislike'),

    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),

    url(r'^(?P<pk>\d+)/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
)
