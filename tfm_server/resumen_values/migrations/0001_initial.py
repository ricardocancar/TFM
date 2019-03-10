# Generated by Django 2.1.5 on 2019-02-21 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resumen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('numbers', models.DecimalField(decimal_places=13, max_digits=100)),
            ],
        ),
    ]
