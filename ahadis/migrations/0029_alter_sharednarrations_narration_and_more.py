# Generated by Django 4.2.3 on 2024-08-03 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ahadis', '0028_sharednarrations_receiver_narration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharednarrations',
            name='narration',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ahadis.narration'),
        ),
        migrations.AlterField(
            model_name='sharednarrations',
            name='receiver_narration',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shared_narrations', to='ahadis.narration'),
        ),
    ]
