from pprint import pprint

from django.urls import path, include
from rest_framework import routers

from ugc.views import *

router = routers.DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'tagged_items', TaggedItemViewSet)
router.register(r'topics', TopicItemViewSet)
router.register(r'scores', ScoreItemViewSet)

pprint(router.urls)

urlpatterns = [
    path('ugc/', include(router.urls)),
]



