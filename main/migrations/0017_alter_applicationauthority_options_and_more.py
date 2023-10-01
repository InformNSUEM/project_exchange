# Generated by Django 4.1.6 on 2023-09-29 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_rename_goal_applicationauthority_purpose_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicationauthority',
            options={'verbose_name': 'Заявки от коммерческого сектора', 'verbose_name_plural': 'Заявки от коммерческого сектора'},
        ),
        migrations.CreateModel(
            name='ApplicationBuisness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.CharField(max_length=150, verbose_name='Заказчик')),
                ('department', models.CharField(max_length=150, verbose_name='Структурное подразделение')),
                ('fio', models.CharField(max_length=150, verbose_name='ФИО заказчика')),
                ('post', models.CharField(max_length=150, verbose_name='Должность ответственного от заказчика')),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, verbose_name='Телефон ответственного от заказчика')),
                ('mail', models.EmailField(max_length=254, verbose_name='Электронная почта ответственного от заказчика')),
                ('task_formulation', models.TextField(verbose_name='Формулировка задачи')),
                ('problem_formulation', models.TextField(verbose_name='Постановка задачи')),
                ('relevance', models.TextField(verbose_name='Актуальность и источники информации')),
                ('completion_dates', models.DateField(verbose_name='Сроки завершения работы над задачей')),
                ('research_purpose', models.TextField(blank=True, null=True, verbose_name='Этапы решения задачи')),
                ('key_words', models.CharField(blank=True, max_length=150, null=True, verbose_name='Ключевые слова')),
                ('wish_result', models.CharField(blank=True, max_length=150, null=True, verbose_name='Ожидаемый результат')),
                ('other_info', models.TextField(blank=True, null=True, verbose_name='Прочая информация')),
                ('depthTask', models.ManyToManyField(related_name='applicationBuisness_depthTash', to='main.depthtask', verbose_name='Глубина проработки задачи')),
                ('program', models.ManyToManyField(blank=True, related_name='applicationBuisness_program', to='main.program', verbose_name='Направления, специальности')),
                ('purpose', models.ManyToManyField(related_name='applicationBuisness_customerGoal', to='main.customergoal', verbose_name='Целеполагание заказчика')),
            ],
        ),
    ]