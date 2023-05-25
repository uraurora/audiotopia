from typing import List

from django.db.models import Model
from rest_framework import serializers

from base.serializers import BASE_FIELDS, BASE_READ_ONLY_FIELDS, UserSerializer
from ugc.models.score import ScoreItem


class ScoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = ScoreItem
        fields: List[str] = BASE_FIELDS + ['user', 'score', 'content_type', 'object_id']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    user = UserSerializer(read_only=True)