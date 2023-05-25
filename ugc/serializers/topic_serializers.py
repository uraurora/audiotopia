from typing import List

from django.db.models import Model
from rest_framework import serializers

from base.serializers import BASE_FIELDS, BASE_READ_ONLY_FIELDS
from ugc.models.topic import Topic, TopicItem


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Topic
        fields: List[str] = BASE_FIELDS + ['name']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS


class TopicItemSerializer(serializers.ModelSerializer):
    """
    A `TaggedItem` serializer with a `GenericRelatedField` mapping all possible
    models to their respective serializers.
    """

    class Meta:
        model: Model = TopicItem
        fields: List[str] = BASE_FIELDS + ['topic', 'content_type', 'object_id']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    tag = TopicSerializer()