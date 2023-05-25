from typing import List

from django.db.models import Model
from rest_framework import serializers

from ai.models.category import Category
from base.serializers import BASE_READ_ONLY_FIELDS


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Category
        fields: List[str] = ['id', 'name', 'icon', 'parent']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS
