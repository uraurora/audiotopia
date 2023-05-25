from rest_framework.viewsets import ModelViewSet

from ai.models.category import Category
from ai.models.licence import Licence
from ai.models.modeling import AIModel, ModelSku
from ai.serializers.category_serializers import CategorySerializer
from ai.serializers.licence_serializers import LicenceSerializer
from ai.serializers.modeling_serializers import AIModelSerializer, ModelSkuSerializer


# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # permission_classes = [permissions.IsAuthenticated]


class LicenceViewSet(ModelViewSet):
    queryset = Licence.objects.all()
    serializer_class = LicenceSerializer

    # permission_classes = [permissions.IsAuthenticated]


class AIModelViewSet(ModelViewSet):
    queryset = AIModel.objects \
        .select_related('category', 'license', 'publish_user') \
        .all()
    serializer_class = AIModelSerializer

    # permission_classes = [permissions.IsAuthenticated]


class ModelSkuViewSet(ModelViewSet):
    queryset = ModelSku.objects \
        .select_related('model') \
        .all()
    serializer_class = ModelSkuSerializer

    # permission_classes = [permissions.IsAuthenticated]
