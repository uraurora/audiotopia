from datetime import datetime, timedelta
import datetime
import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ai.models import *
from ugc.models import TaggedItem


# Create your tests here.
class AIModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test_user', email='zzrzhezhiren@gmail.com', password='test_user')
        user: User = User.objects.first()

        Licence.objects.create(id=uuid.uuid4(),
                               name='test_Licence1',
                               description='test_Licence1',
                               content='apache licence 2.0',
                               )
        licence: Licence = Licence.objects.first()
        print(licence.id)
        Category.objects.create(id=uuid.uuid4(),
                                name='test_Category1',
                                description='test_Category1',
                                )
        category: Category = Category.objects.first()
        print(category.id)

        for i in range(0, 5):
            AIModel.objects.create(id=uuid.uuid4(),
                                   name=f'vits_{i}',
                                   description=f'vits_{i} test',
                                   category_id=category.id,
                                   license_id=licence.id,
                                   publish_user_id=user.id,
                                   )
        model: AIModel = AIModel.objects.all()

    def test_generic_query(self):
        content_type: ContentType = ContentType.objects.get_for_model(AIModel)
        TaggedItem.objects \
            .select_related("tag") \
            .filter(
            content_type=content_type,
            object_pk=uuid.uuid4
        )

    def tearDown(self):
        # AIModel.objects.all().delete()
        pass

    def test_something(self):
        AIModel.objects.filter(create_time__date__gte=datetime.date(2023, 5, 18)).first().delete()

        license: Licence = Licence.objects.first()
        print(license.aimodel_set.all())

        category: Category = Category.objects.first()
        print(category.aimodel_set.all())
