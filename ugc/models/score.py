from django.conf import settings
from django.db import models

from base.models import BaseModel, GenericBaseModel, GLOBAL_USER


# <editor-fold desc='managers'>

# </editor-fold>

# <editor-fold desc='models'>
class ScoreItem(GenericBaseModel):
    user = models.ForeignKey(GLOBAL_USER, on_delete=models.DO_NOTHING, verbose_name='user')
    score = models.DecimalField(
        choices=BaseModel.SCORE_CHOICES_LIST,
        decimal_places=1,
        max_digits=2,
        null=False,
        default=0.0,
        verbose_name='score'
    )

    def __str__(self):
        return str(self.score)

    class Meta:
        db_table = 'ugc_score_item'
        db_table_comment = 'score item'
        db_tablespace = 'ai_score'
        unique_together = ('user', 'score',)

        indexes = [
            models.Index(fields=['user', 'score'], name='idx_user_score', db_tablespace=db_tablespace),
        ]

# </editor-fold>
