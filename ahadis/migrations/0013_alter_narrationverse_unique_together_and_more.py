# Generated by Django 4.1.4 on 2023-02-04 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0012_alter_contentsummarytree_narration_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='narrationverse',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='narrationverse',
            name='content_summary_tree',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ahadis.contentsummarytree'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='narrationverse',
            unique_together={('content_summary_tree', 'quran_verse')},
        ),
        migrations.RemoveField(
            model_name='narrationverse',
            name='narration',
        ),
    ]
