from typing import List

from django.db.models import Model
from rest_framework import serializers

from ai.models.modeling import AIModel, ModelSku
from ai.serializers.category_serializers import CategorySerializer
from ai.serializers.licence_serializers import LicenceSerializer
from base.serializers import BASE_READ_ONLY_FIELDS, BASE_FIELDS, UserSerializer


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = AIModel
        fields: List[str] = BASE_FIELDS + ['name', 'slug', 'category', 'license', 'publish_user']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    category = CategorySerializer(read_only=True)
    license = LicenceSerializer(read_only=True)
    publish_user = UserSerializer(read_only=True)


class ModelSkuSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = ModelSku
        fields: List[str] = BASE_FIELDS + ['model', 'version', 'size', 'url', 'encryption']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    model = AIModelSerializer(read_only=True)
