from django.db import models

from base.models import BaseModel


class Licence(BaseModel):
    name = models.CharField(max_length=BaseModel.TITLE_LENGTH, null=False, default='', verbose_name='name')
    content = models.TextField(null=False, default='', verbose_name='content')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ai_model_licence'
        db_table_comment = 'licence table'
        db_tablespace = 'ai_model_licence'
