from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from ai.models.category import Category
from ai.models.licence import Licence
from ai.models.modeling import AIModel, ModelSku


# Register your models here.

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'create_time', 'update_time')
    list_filter = ['category']
    search_fields = ('name', 'category__name', 'licence__name', 'topic__name')


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Licence)
admin.site.register(ModelSku)
