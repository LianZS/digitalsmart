# Generated by Django 2.2.3 on 2019-07-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0011_auto_20190723_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablemanager',
            name='last_date',
            field=models.IntegerField(verbose_name='最近更新时间--时间戳，根据时间戳查找数据'),
        ),
    ]