# Generated by Django 4.1.4 on 2023-05-25 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0015_book1_contentsummarytree1_imam1_narration1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='narration1',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ahadis.book1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='narration1',
            name='imam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ahadis.imam1'),
            preserve_default=False,
        ),
    ]
