# Generated by Django 4.2.1 on 2023-05-23 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='pk')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update_time')),
                ('name', models.SlugField(max_length=100)),
            ],
            options={
                'db_table': 'ugc_model_tag',
                'db_table_comment': 'common tag table',
                'db_tablespace': 'ugc_model_tag',
            },
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='pk')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update_time')),
                ('object_pk', models.UUIDField(db_index=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.tag')),
            ],
            options={
                'db_table': 'ugc_model_tagged_item',
                'db_table_comment': 'common tagged item table',
                'db_tablespace': 'ugc_model_tagged_item',
            },
        ),
    ]
