# Generated by Django 4.1.4 on 2023-01-14 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0006_quranverse_narrationsubject_narrationfootnote_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentsummarytree',
            name='alphabet',
            field=models.CharField(default='nulll', max_length=5),
            preserve_default=False,
        ),
    ]
