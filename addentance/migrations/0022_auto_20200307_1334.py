# Generated by Django 2.2.4 on 2020-03-07 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addentance', '0021_auto_20200306_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='detailed_attendance',
            field=models.ManyToManyField(blank=True, null=True, to='addentance.AttendanceTimestamp'),
        ),
    ]
