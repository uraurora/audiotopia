from django.db import models

from base.models import BaseModel, GenericBaseModel


# <editor-fold desc='managers'>

# </editor-fold>

# <editor-fold desc='models'>
class Topic(BaseModel):
    name = models.SlugField(max_length=BaseModel.TAG_LENGTH, null=False, blank=False, verbose_name='name')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ugc_topic'
        db_table_comment = 'topic which users can subscribe'
        db_tablespace = 'ugc_topic'

        indexes = [
            models.Index(fields=['name'], name='idx_name', db_tablespace=db_tablespace),
        ]


class TopicItem(GenericBaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic.name

    class Meta:
        db_table = 'ugc_topic_item'
        db_table_comment = 'topic item which users can subscribe'
        db_tablespace = 'ugc_topic_item'

# </editor-fold>
