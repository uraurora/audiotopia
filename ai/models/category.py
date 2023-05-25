from django.db import models
from mptt.fields import TreeForeignKey

from mptt.managers import TreeManager
from mptt.models import MPTTModel

from base.models import BaseModel


class Category(MPTTModel, BaseModel):
    objects = TreeManager()

    name = models.CharField(max_length=BaseModel.TITLE_LENGTH)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.URLField(max_length=BaseModel.URL_LENGTH, blank=True, default='', verbose_name='icon')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'ai_model_category'
        db_table_comment = 'model category table'
        db_tablespace = 'ai_model_category'

        indexes = [
            models.Index(fields=['name', 'parent'], name='idx_name_parent', db_tablespace=db_tablespace),
        ]
