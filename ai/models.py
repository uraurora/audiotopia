import django.db.models as dj_models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_comments.models import Comment
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from base.models import BaseModel
from ugc.models import Tag, TaggedItem

# Create your models here.
GlobalUser = settings.AUTH_USER_MODEL


class Category(MPTTModel, BaseModel):
    objects = TreeManager()

    name = models.CharField(max_length=BaseModel.TITLE_LENGTH)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.URLField(max_length=BaseModel.URL_LENGTH, blank=True, default='', verbose_name='url')

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


class Licence(BaseModel):
    name = models.CharField(max_length=BaseModel.TITLE_LENGTH, null=False, default='', verbose_name='name')
    content = models.TextField(null=False, default='', verbose_name='content')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ai_model_licence'
        db_table_comment = 'licence table'
        db_tablespace = 'ai_model_licence'


class AIModel(BaseModel):
    name = models.CharField(max_length=BaseModel.TITLE_LENGTH)
    slug = models.SlugField(max_length=BaseModel.TITLE_LENGTH, null=False, default='-', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    license = models.ForeignKey(Licence, on_delete=models.DO_NOTHING, null=True)
    tags = GenericRelation(
        TaggedItem,
        content_type_field='content_type',
        object_id_field='object_pk'
    )
    comments = GenericRelation(
        Comment,
        content_type_field='content_type',
        object_id_field='object_pk'
    )
    publish_user = models.ForeignKey(
        GlobalUser,
        on_delete=models.DO_NOTHING,
        related_name='publish_user',
        verbose_name='publisher'
    )
    subscribed_users = models.ManyToManyField(
        GlobalUser,
        through='Subscription',
        related_name='subscribed_users',
        verbose_name='subscribed users'
    )

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


class Topic(BaseModel):
    name = models.CharField(max_length=BaseModel.TITLE_LENGTH, null=False, blank=False, verbose_name='name')
    models = models.ManyToManyField(AIModel, through='Subscription', verbose_name='models')
    users = dj_models.ManyToManyField(GlobalUser, through='Subscription', verbose_name='users')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ai_topic'
        db_table_comment = 'topic which users can subscribe'
        db_tablespace = 'ai_topic'

        indexes = [
            models.Index(fields=['name'], name='idx_name', db_tablespace=db_tablespace),
        ]


class Subscription(BaseModel):
    user = models.ForeignKey(GlobalUser, on_delete=models.DO_NOTHING, verbose_name='user')
    model = models.ForeignKey(AIModel, on_delete=models.DO_NOTHING, verbose_name='model')
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, null=True, verbose_name='topic')

    class Meta:
        db_table = 'ai_subscription'
        db_table_comment = 'user subscription'
        db_tablespace = 'ai_subscription'
        unique_together = ('user', 'model', 'topic',)

        indexes = [
            models.Index(fields=['user', 'model', 'topic'], name='idx_user_model_topic', db_tablespace=db_tablespace),
        ]


class Score(BaseModel):
    user = models.ForeignKey(GlobalUser, on_delete=models.DO_NOTHING, verbose_name='user')
    model = models.ForeignKey(AIModel, on_delete=models.DO_NOTHING, verbose_name='model')
    score = models.DecimalField(choices=BaseModel.SCORE_CHOICES_LIST, decimal_places=1, max_digits=2, null=False,
                                default=0.0, verbose_name='score')

    def __str__(self):
        return str(self.score)

    class Meta:
        db_table = 'ai_score'
        db_table_comment = 'user score'
        db_tablespace = 'ai_score'
        unique_together = ('user', 'model',)

        indexes = [
            models.Index(fields=['user', 'model'], name='idx_user_model', db_tablespace=db_tablespace),
        ]
