# Generated by Django 4.1.4 on 2023-02-04 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0013_alter_narrationverse_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='narrationverse',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='narrationverse',
            name='narration',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ahadis.narration'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='narrationverse',
            unique_together={('narration', 'quran_verse')},
        ),
        migrations.RemoveField(
            model_name='narrationverse',
            name='content_summary_tree',
        ),
        migrations.CreateModel(
            name='NarrationSubjectVerse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('content_summary_tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ahadis.contentsummarytree')),
                ('quran_verse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ahadis.quranverse')),
            ],
            options={
                'db_table': 'NarrationSubjectVerse',
                'unique_together': {('content_summary_tree', 'quran_verse')},
            },
        ),
    ]