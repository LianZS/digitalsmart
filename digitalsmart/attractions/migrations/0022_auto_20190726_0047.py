# Generated by Django 2.2.3 on 2019-07-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0021_userprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(null=True, upload_to='photo'),
        ),
    ]