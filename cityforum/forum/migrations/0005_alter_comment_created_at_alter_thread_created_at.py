# Generated by Django 4.1.7 on 2023-03-31 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]