# Generated by Django 2.2.6 on 2019-10-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='haha',
            field=models.CharField(default='aaa', max_length=30, verbose_name='hehehe'),
        ),
    ]
