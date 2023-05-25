from uuid import UUID

from django.contrib.contenttypes.models import ContentType
from django.db import models
from softdelete.models import SoftDeleteManager

from base.models import BaseModel, GenericBaseModel


# <editor-fold desc='managers'>
class TaggedItemManager(SoftDeleteManager):

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
        db_table = 'ugc_tag'
        db_table_comment = 'common tag table'
        db_tablespace = 'ugc_tag'


class TaggedItem(GenericBaseModel):
    objects = TaggedItemManager()

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name

    class Meta:
        db_table = 'ugc_tagged_item'
        db_table_comment = 'common tagged item table'
        db_tablespace = 'ugc_tagged_item'

# </editor-fold>
