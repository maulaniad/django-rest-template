# Generated by Django 5.1 on 2024-09-04 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='asset',
            field=models.DecimalField(decimal_places=0, default=100, max_digits=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='profit',
            field=models.DecimalField(decimal_places=0, default=100, max_digits=20),
            preserve_default=False,
        ),
    ]
