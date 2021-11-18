# Generated by Django 3.2.9 on 2021-11-17 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_alter_womanlike_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='womancomment',
            name='username',
        ),
        migrations.AddField(
            model_name='womancomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]