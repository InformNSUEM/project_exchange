# Generated by Django 4.1.6 on 2023-02-16 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_disciplines_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplines',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование'),
        ),
    ]