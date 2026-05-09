# Hand-written migration: add Project model.

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_public_user_linkedin_username_user_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=120, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=140, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                (
                    'ai_percentage',
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text='Percentage (0-100) of this project written by AI',
                        verbose_name='AI percentage',
                    ),
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('planned', 'Planned'),
                            ('in_progress', 'In progress'),
                            ('completed', 'Completed'),
                            ('archived', 'Archived'),
                        ],
                        default='planned',
                        max_length=20,
                        verbose_name='status',
                    ),
                ),
                ('repo_url', models.URLField(blank=True, verbose_name='repository URL')),
                ('live_url', models.URLField(blank=True, verbose_name='live URL')),
                (
                    'created_at',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='created at',
                    ),
                ),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                (
                    'owner',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='projects',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
                'ordering': ['-updated_at'],
                'unique_together': {('owner', 'slug')},
            },
        ),
    ]
