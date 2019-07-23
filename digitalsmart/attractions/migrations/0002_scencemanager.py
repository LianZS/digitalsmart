# Generated by Django 2.2.3 on 2019-07-23 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScenceManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.SmallIntegerField(verbose_name='标识')),
                ('area', models.CharField(max_length=32, verbose_name='地名')),
                ('longitude', models.FloatField(verbose_name='中心经度')),
                ('latitude', models.FloatField(verbose_name='中心纬度')),
                ('loaction', models.CharField(max_length=18, verbose_name='所处城市')),
                ('citypid', models.IntegerField(verbose_name='所处城市标识')),
                ('weatherpid', models.TextField(verbose_name='对应的天气标识')),
                ('flag', models.SmallIntegerField(verbose_name='类别标识,百度数据为1，腾讯为0')),
            ],
            options={
                'db_table': 'scencemanager',
            },
        ),
    ]
