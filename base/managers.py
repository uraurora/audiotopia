from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class LogisticQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class MyBaseManager(BaseManager.from_queryset(LogisticQuerySet)):

    def __init__(self, *args, **kwargs):
        self.__add_is_deleted_filter = True
        super(MyBaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        # 这一步是后面的filter方法会调用的，所以这里不胿忘记要重写
        queryset = super(MyBaseManager, self).get_queryset(*args, **kwargs)

        # 判断用户是否主动传入is_deleted的筛选条件，如果主动传入，就不做自动筛选操作
        if self.__add_is_deleted_filter:
            # 过滤掉已删除的记录
            queryset = queryset.filter(is_deleted=False)

        return queryset

    def filter(self, *args, **kwargs):

        # 判断用户是否主动传入is_deleted的筛选条件，如果主动传入，就不做自动筛选操作
        if not kwargs.get('is_deleted') is None:
            self.__add_is_deleted_filter = False
        f = super(MyBaseManager, self).filter(*args, **kwargs)
        return f
