# Generated by Django 2.2.3 on 2019-07-23 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scenceflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.SmallIntegerField(verbose_name='标识')),
                ('ddate', models.IntegerField(verbose_name='日期')),
                ('ttime', models.TimeField(verbose_name='时间')),
                ('num', models.IntegerField(verbose_name='总人数')),
            ],
            options={
                'db_table': 'scenceflow',
                'unique_together': {('pid', 'ddate', 'ttime', 'num')},
            },
        ),
    ]
