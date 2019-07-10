# Generated by Django 2.2.3 on 2019-07-10 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attractions', '0002_delete_scenceflow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenceflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('scenceid', models.IntegerField()),
                ('date', models.DateField()),
                ('detailtime', models.CharField(max_length=32)),
                ('num', models.IntegerField()),
            ],
            options={
                'db_table': 'scenceflow',
                'unique_together': {('scenceid', 'date', 'detailtime', 'num')},
            },
        ),
    ]
