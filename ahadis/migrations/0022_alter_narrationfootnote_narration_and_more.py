# Generated by Django 4.2.3 on 2023-07-29 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0021_delete_contentsummarytree1_remove_narration1_book_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='narrationfootnote',
            name='narration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='footnotes', to='ahadis.narration'),
        ),
        migrations.AlterField(
            model_name='narrationsubject',
            name='narration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='ahadis.narration'),
        ),
        migrations.AlterField(
            model_name='narrationsubjectverse',
            name='content_summary_tree',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verse', to='ahadis.contentsummarytree'),
        ),
    ]