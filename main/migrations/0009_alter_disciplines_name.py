# Generated by Django 4.1.6 on 2023-02-16 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_applicationauthorityprocessing_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplines',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Наименование'),
        ),
    ]