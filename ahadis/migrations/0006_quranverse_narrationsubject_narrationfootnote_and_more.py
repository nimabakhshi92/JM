# Generated by Django 4.1.4 on 2022-12-27 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0005_rename_book_id_narration_book_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuranVerse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_no', models.IntegerField()),
                ('page_no', models.IntegerField()),
                ('surah_no', models.IntegerField()),
                ('verse_no', models.IntegerField()),
                ('surah_name', models.CharField(max_length=100)),
                ('verse_content', models.TextField()),
            ],
            options={
                'db_table': 'QuranVerse',
            },
        ),
        migrations.CreateModel(
            name='NarrationSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('narration', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ahadis.narration')),
            ],
            options={
                'db_table': 'NarrationSubject',
            },
        ),
        migrations.CreateModel(
            name='NarrationFootnote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.TextField()),
                ('explanation', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('narration', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ahadis.narration')),
            ],
            options={
                'db_table': 'NarrationFootnote',
            },
        ),
        migrations.CreateModel(
            name='ContentSummaryTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_1', models.CharField(max_length=200)),
                ('subject_2', models.CharField(max_length=200)),
                ('subject_3', models.CharField(max_length=200)),
                ('subject_4', models.CharField(max_length=200)),
                ('subject_5', models.TextField()),
                ('summary', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('narration', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ahadis.narration')),
            ],
            options={
                'db_table': 'ContentSummaryTree',
            },
        ),
        migrations.CreateModel(
            name='NarrationVerse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('narration', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ahadis.narration')),
                ('quran_verse', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ahadis.quranverse')),
            ],
            options={
                'db_table': 'NarrationVerse',
                'unique_together': {('narration', 'quran_verse')},
            },
        ),
    ]
