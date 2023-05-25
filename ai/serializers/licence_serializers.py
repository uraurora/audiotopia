from typing import List

from django.db.models import Model
from rest_framework import serializers

from ai.models.licence import Licence
from base.serializers import BASE_READ_ONLY_FIELDS


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Licence
        fields: List[str] = ['id', 'name', 'content']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS
