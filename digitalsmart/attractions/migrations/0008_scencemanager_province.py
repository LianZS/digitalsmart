# Generated by Django 2.2.3 on 2019-07-23 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0007_peopleposition0_peopleposition1_peopleposition2_peopleposition3_peopleposition4_peopleposition5_peop'),
    ]

    operations = [
        migrations.AddField(
            model_name='scencemanager',
            name='province',
            field=models.CharField(default=' ', max_length=18, verbose_name='省份'),
            preserve_default=False,
        ),
    ]
