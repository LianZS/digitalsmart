# Generated by Django 2.2.3 on 2019-08-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scencemanager',
            name='type_flag',
            field=models.SmallIntegerField(db_column='type_flag', default=1, verbose_name='类别标识,百度数据为1，腾讯为0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scencemanager',
            name='flag',
            field=models.SmallIntegerField(db_column='flag', verbose_name='是否公开，0表示公开'),
        ),
        migrations.AlterField(
            model_name='searchrate',
            name='flag',
            field=models.SmallIntegerField(db_column='flag', default=0, verbose_name='是否公开'),
        ),
    ]