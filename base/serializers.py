from typing import List

from django.contrib.auth import get_user_model
from django.db.models import Model
from rest_framework import serializers

BASE_FIELDS: List[str] = ['id', 'description', 'create_time', 'update_time']

BASE_READ_ONLY_FIELDS: List[str] = ['id', 'create_time', 'update_time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = get_user_model()
        fields: List[str] = ['username', 'email', 'is_staff', 'is_active', 'is_superuser',
                             'first_name', 'last_name', 'date_joined', 'last_login']
        read_only_fields: List[str] = ['date_joined', 'last_login']
