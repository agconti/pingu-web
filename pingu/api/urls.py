from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
import views

router = DefaultRouter()
router.register(r'match', views.MatchViewSet)
router.register(r'rankings', views.RankingViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.ObtainAuthTokenView.as_view(), name="auth-token"),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/login/?$', views.UserLogin.as_view(), name='user-login'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/(?P<pk>[0-9]+)/change_password$', views.ChangePasswordView.as_view(), name='user-change_password'),
    url(r'^create-match/$', views.MatchResultsView.as_view(), name="create-match")
)
