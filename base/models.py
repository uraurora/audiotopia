from decimal import Decimal

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from softdelete.models import SoftDeleteObject, SoftDeleteManager

from typing import List, Dict, Tuple

import uuid


GLOBAL_USER = settings.AUTH_USER_MODEL

# Create your models here.
class BaseModel(SoftDeleteObject, models.Model):
    objects = SoftDeleteManager()

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name='pk',
        default=uuid.uuid4
    )
    description = models.TextField(blank=True, default='', verbose_name='description')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create_time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='update_time')

    TITLE_LENGTH: int = 255

    TAG_LENGTH: int = 100

    URL_LENGTH: int = 512

    ENCRYPTION_LENGTH: int = 128

    SCORE_CHOICES_LIST: List[Tuple[Decimal, str]] = [
        (Decimal(0.0), '0.0'), (Decimal(0.5), '0.5'),

        (Decimal(1.0), '1.0'), (Decimal(1.5), '1.5'),

        (Decimal(2.0), '2.0'), (Decimal(2.5), '2.5'),

        (Decimal(3.0), '3.0'), (Decimal(3.5), '3.5'),

        (Decimal(4.0), '4.0'), (Decimal(4.5), '4.5'),

        (Decimal(5.0), '5.0')

    ]

    FILE_TYPE_DICT: Dict[str, List[str]] = {
        'image': ['jpg', 'jpeg', 'png', 'bmp', 'gif'],
        'video': ['mp4', 'avi', 'rmvb', 'mkv', 'flv', 'wmv', 'mov'],
        'audio': ['mp3', 'wav', 'wma', 'aac', 'flac', 'ape', 'ogg'],
        'document': ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'txt'],
        'binary': ['exe', 'dll', 'so', 'bin', 'msi', 'jar', 'zip', 'rar', '7z', 'gz', 'bz2', 'tar', 'iso'],
        'compressed': ['gz', 'bz2', 'tar', '7z', 'iso'],
        'other': ['*']
    }

    FILE_TYPE_LIST: List[Tuple[str, str]] = [
        ('image', 'image'),
        ('video', 'video'),
        ('audio', 'audio'),
        ('document', 'document'),
        ('binary', 'binary'),
        ('compressed', 'compressed'),
        ('other', 'other')
    ]

    def is_deleted(self) -> bool:
        return self.get_deleted()

    class Meta:
        abstract: bool = True


class GenericBaseModel(BaseModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(db_index=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    class Meta:
        abstract: bool = True

        indexes = [
            models.Index(fields=['content_type', 'object_id'])
        ]
