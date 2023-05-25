from pprint import pprint

from django.urls import path, include
from rest_framework import routers

from ai.views import *

router = routers.DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'licences', LicenceViewSet)
router.register(r'models', AIModelViewSet)
router.register(r'model_skus', ModelSkuViewSet)

pprint(router.urls)

urlpatterns = [
    path('ai/', include(router.urls)),
]



