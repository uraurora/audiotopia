from uuid import UUID

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_comments.models import Comment
from mptt.models import MPTTModel

from base.managers import MyBaseManager
from base.models import BaseModel


# <editor-fold desc='managers'>
class TaggedItemManager(MyBaseManager):

    def get_tag_for(self, obj_type, obj_id: UUID):
        content_type = ContentType.objects.get_for_model(obj_type)

        queryset = TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                content_pk=obj_id
            )
        return queryset

# </editor-fold>

# <editor-fold desc='models'>


class Tag(BaseModel):
    name = models.SlugField(max_length=BaseModel.TAG_LENGTH)

    class Meta:
        db_table = 'ugc_model_tag'
        db_table_comment = 'common tag table'
        db_tablespace = 'ugc_model_tag'


class TaggedItem(BaseModel):
    objects = TaggedItemManager()

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.UUIDField(db_index=True)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    def __str__(self):
        return self.tag.name

    class Meta:
        db_table = 'ugc_model_tagged_item'
        db_table_comment = 'common tagged item table'
        db_tablespace = 'ugc_model_tagged_item'
# </editor-fold>
