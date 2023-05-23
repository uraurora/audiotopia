from django.db import models

from base.models import BaseModel


# Create your models here.
class Media(BaseModel):
    url = models.URLField(max_length=BaseModel.URL_LENGTH, blank=True, default='', verbose_name='url')
    file_name = models.CharField(max_length=BaseModel.TITLE_LENGTH)
    file_type = models.CharField(max_length=BaseModel.TITLE_LENGTH, choices=BaseModel.FILE_TYPE_LIST)
    size = models.PositiveBigIntegerField(
        null=False,
        blank=True,
        default=0,
        verbose_name='size/B',
        db_comment='storage size, unit: B'
    )
    duration = models.BigIntegerField(
        null=False,
        blank=True,
        default=0,
        verbose_name='duration/ms',
        db_comment='duration of media, unit: ms'
    )
