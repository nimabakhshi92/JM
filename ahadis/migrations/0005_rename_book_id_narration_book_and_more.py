# Generated by Django 4.1.4 on 2022-12-27 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0004_narration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='narration',
            old_name='book_id',
            new_name='book',
        ),
        migrations.RenameField(
            model_name='narration',
            old_name='imam_id',
            new_name='imam',
        ),
    ]
