from rest_framework import routers

from modules.content.views import HomeViewSet, EventViewSet, PageViewSet 
from modules.users.views import InscriptionViewSet

router = routers.DefaultRouter()


# Content
router.register('home', HomeViewSet, basename='home')
router.register('event', EventViewSet, basename='event')
router.register('page', PageViewSet, basename='page')
router.register('inscription', InscriptionViewSet, basename='inscription')


urls = router.urls
