from typing import List

from django.db.models import Model
from django_comments.models import Comment
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from ugc.models import *
from ai.models import AIModel
from ai.serializers import AIModelSerializer

BASE_FIELDS: List[str] = ['id', 'description', 'created_time', 'updated_time']

BASE_READ_ONLY_FIELDS: List[str] = ['id', 'created_time', 'updated_time']


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
    content_object = GenericRelatedField({
        AIModel: AIModelSerializer(),

    })
    tag = TagSerializer()

    class Meta:
        model: Model = TaggedItem
        fields: List[str] = BASE_FIELDS + ['tag', 'content_type', 'object_pk', 'content_object']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS


class CommentSerializer(serializers.ModelSerializer):

    content_object = GenericRelatedField({
        AIModel: AIModelSerializer(),

    })

    class Meta:
        model: Model = Comment
        fields: List[str] = ['id', 'content_type', 'object_pk', 'user', 'user_name', 'user_email', 'user_url',
                             'comment', 'submit_date', 'ip_address', 'is_public', 'is_removed', 'site']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS
