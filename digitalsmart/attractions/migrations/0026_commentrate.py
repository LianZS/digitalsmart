# Generated by Django 2.2.3 on 2019-08-11 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0025_scenceimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(db_column='pid')),
                ('adjectives', models.CharField(db_column='adjectives', max_length=16, verbose_name='形容词')),
                ('rate', models.FloatField(db_column='rate', verbose_name='评分')),
            ],
            options={
                'db_table': 'comment_rate',
            },
        ),
    ]
