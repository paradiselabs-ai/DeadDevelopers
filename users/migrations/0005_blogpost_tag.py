# Hand-written migration: add Tag + BlogPost models.

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
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
                ('name', models.CharField(max_length=40, unique=True, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=50, unique=True, verbose_name='slug')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
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
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(blank=True, max_length=220, verbose_name='slug')),
                (
                    'excerpt',
                    models.CharField(
                        blank=True,
                        help_text='Short summary shown on listing pages',
                        max_length=400,
                        verbose_name='excerpt',
                    ),
                ),
                (
                    'content',
                    models.TextField(
                        help_text='Markdown — rendered through the same XSS sanitizer as portfolios',
                        verbose_name='content',
                    ),
                ),
                ('is_published', models.BooleanField(default=False, verbose_name='published')),
                (
                    'published_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='published at'),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='created at',
                    ),
                ),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='view count')),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='blog_posts',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'tags',
                    models.ManyToManyField(
                        blank=True,
                        related_name='posts',
                        to='users.tag',
                    ),
                ),
            ],
            options={
                'verbose_name': 'blog post',
                'verbose_name_plural': 'blog posts',
                'ordering': ['-published_at', '-created_at'],
                'unique_together': {('author', 'slug')},
                'indexes': [
                    models.Index(fields=['-published_at'], name='users_blogp_publish_d4e0a6_idx'),
                    models.Index(fields=['author', 'is_published'], name='users_blogp_author__b3e7c8_idx'),
                ],
            },
        ),
    ]
