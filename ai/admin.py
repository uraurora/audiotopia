from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from ai import models


# Register your models here.

@admin.register(models.AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'create_time', 'update_time')
    list_filter = ['category']
    search_fields = ('name', 'category__name', 'licence__name', 'topic__name')


admin.site.register(models.Category, MPTTModelAdmin)
admin.site.register(models.Licence)
admin.site.register(models.ModelSku)
admin.site.register(models.Topic)
admin.site.register(models.Score)
admin.site.register(models.Subscription)
