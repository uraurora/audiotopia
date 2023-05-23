from typing import List

from rest_framework import serializers
from django.db.models import Model

from ai.models import *

from ugc.serializers import TaggedItemSerializer, CommentSerializer

BASE_FIELDS: List[str] = ['id', 'description', 'created_time', 'updated_time']

BASE_READ_ONLY_FIELDS: List[str] = ['id', 'created_time', 'updated_time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = GlobalUser
        fields: List[str] = ['username', 'email', 'is_staff', 'is_active', 'is_superuser',
                             'first_name', 'last_name', 'date_joined', 'last_login']
        read_only_fields: List[str] = ['date_joined', 'last_login']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Category
        fields: List[str] = BASE_FIELDS + ['name', 'icon', 'parent']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Licence
        fields: List[str] = BASE_FIELDS + ['name', 'content']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = AIModel
        fields: List[str] = BASE_FIELDS + \
                            ['name', 'slug', 'category', 'licence', 'tags',
                             'comments', 'publish_user', 'subscribed_users']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    category = CategorySerializer(read_only=True)
    licence = LicenceSerializer(read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    # comments = serializers.SlugRelatedField(many=True, read_only=True,  slug_field='id')
    publish_user = UserSerializer(read_only=True)
    subscribed_users = UserSerializer(many=True, read_only=True)


class ModelSkuSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = ModelSku
        fields: List[str] = BASE_FIELDS + ['model', 'version', 'size', 'url', 'encryption']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    model = AIModelSerializer(read_only=True)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Topic
        fields: List[str] = BASE_FIELDS + ['name', 'models', 'users']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    models = AIModelSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Subscription
        fields: List[str] = BASE_FIELDS + ['user', 'model', 'topic']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    user = UserSerializer(read_only=True)
    model = AIModelSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = Score
        fields: List[str] = BASE_FIELDS + ['user', 'model', 'score']
        read_only_fields: List[str] = BASE_READ_ONLY_FIELDS

    user = UserSerializer(read_only=True)
    model = AIModelSerializer(read_only=True)
