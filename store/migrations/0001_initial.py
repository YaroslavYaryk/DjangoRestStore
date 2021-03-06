# Generated by Django 3.2.9 on 2021-11-17 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='author_name')),
                ('age', models.IntegerField(verbose_name='author_age')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
                ('rate', models.CharField(choices=[('1', 'Awful'), ('2', 'Low'), ('3', 'Medium'), ('4', 'Good'), ('5', 'Perfect')], max_length=250, verbose_name='rate')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
                ('ico', models.ImageField(blank=True, null=True, upload_to='icons/Data%y/%m/%d/')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField(verbose_name='rating_star')),
            ],
        ),
        migrations.CreateModel(
            name='Woman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('updation_date', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, upload_to='photos/Data%y/%m/%d/')),
                ('is_published', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.author', verbose_name='Author')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'New',
                'verbose_name_plural': 'News',
                'ordering': ['-creation_date'],
                'get_latest_by': 'creation_date',
            },
        ),
        migrations.CreateModel(
            name='WomanLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='store.woman')),
                ('rating', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating_star', to='store.rating')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='woman_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WomanImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(upload_to='photos/Data%y/%m/%d/')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.woman')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WomanComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('comment', models.TextField(max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_comments', to='store.woman')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='LikedComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('choice', models.CharField(default='No', max_length=50)),
                ('post_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_comment', to='store.womancomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
                ('post_news', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ip', to='store.woman')),
            ],
        ),
    ]
