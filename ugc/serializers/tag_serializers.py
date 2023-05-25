from typing import List

from django.db.models import Model
from rest_framework import serializers

from base.serializers import BASE_FIELDS, BASE_READ_ONLY_FIELDS
from ugc.models.tag import Tag, TaggedItem


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Tag
        fields: List[str] = BASE_FIELDS + ['name']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS


class TaggedItemSerializer(serializers.ModelSerializer):
    """
    A `TaggedItem` serializer with a `GenericRelatedField` mapping all possible
    models to their respective serializers.
    """

    class Meta:
        model: Model = TaggedItem
        fields: List[str] = BASE_FIELDS + ['tag', 'content_type', 'object_id']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    tag = TagSerializer()

# :todo

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: Model = Comment
#         fields: List[str] = ['user', 'comment', 'submit_date', 'site', 'content_type', 'object_pk']
#         read_only_fields: List[str] = BASE_READ_ONLY_FIELDS + ['submit_date']
