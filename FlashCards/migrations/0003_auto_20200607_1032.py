# Generated by Django 3.0.5 on 2020-06-07 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlashCards', '0002_auto_20200606_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='back_side_text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='front_side_text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]