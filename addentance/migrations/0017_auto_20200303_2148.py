# Generated by Django 2.2.4 on 2020-03-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addentance', '0016_attendancetimestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetimestamp',
            name='timestamp',
            field=models.DateField(),
        ),
    ]
