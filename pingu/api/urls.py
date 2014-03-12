from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
import views

router = DefaultRouter()
router.register(r'match', views.MatchViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
