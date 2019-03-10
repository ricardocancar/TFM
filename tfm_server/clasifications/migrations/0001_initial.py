# Generated by Django 2.1.5 on 2019-02-18 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clasifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=250)),
                ('path', models.CharField(max_length=250)),
                ('label', models.CharField(max_length=80)),
                ('score', models.DecimalField(decimal_places=13, max_digits=100)),
            ],
        ),
    ]
