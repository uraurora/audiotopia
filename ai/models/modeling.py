from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from ai.models.category import Category
from ai.models.licence import Licence
from base.models import BaseModel, GLOBAL_USER


class AIModel(BaseModel):
    name = models.CharField(max_length=BaseModel.TITLE_LENGTH)
    slug = models.SlugField(max_length=BaseModel.TITLE_LENGTH, null=False, default='-', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    license = models.ForeignKey(Licence, on_delete=models.DO_NOTHING, null=True)
    publish_user = models.ForeignKey(
        GLOBAL_USER,
        on_delete=models.DO_NOTHING,
        related_name='published_model',
        verbose_name='publisher'
    )
    # tags = GenericRelation(
    #     TaggedItem,
    #     content_type_field='content_type',
    #     object_id_field='object_pk'
    # )
    # comments = GenericRelation(
    #     Comment,
    #     content_type_field='content_type',
    #     object_id_field='object_pk'
    # )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'ai_model'
        db_table_comment = 'ai model table'
        db_tablespace = 'ai_model'
        indexes = [
            models.Index(fields=['name', 'category'], name='idx_name_category', db_tablespace=db_tablespace),
        ]
        ordering = ['name', 'category']


class ModelSku(BaseModel):
    model = models.ForeignKey(AIModel, on_delete=models.DO_NOTHING, verbose_name='base ai')
    version = models.CharField(max_length=BaseModel.TITLE_LENGTH, null=False, default='', verbose_name='version')
    size = models.PositiveBigIntegerField(null=False, default=0, verbose_name='storage size')
    url = models.URLField(max_length=BaseModel.URL_LENGTH, blank=True, default='', verbose_name='url')
    encryption = models.CharField(
        max_length=BaseModel.ENCRYPTION_LENGTH,
        null=False,
        default='',
        verbose_name='encryption'
    )

    def __str__(self):
        return self.version

    class Meta:
        db_table = 'ai_model_sku'
        db_table_comment = 'model sku table'
        db_tablespace = 'ai_model_sku'

        indexes = [
            models.Index(fields=['model', 'version'], name='idx_model_version', db_tablespace=db_tablespace),
        ]