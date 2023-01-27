# Generated by Django 4.1.4 on 2022-12-24 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('publisher', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('language', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Book',
            },
        ),
    ]
