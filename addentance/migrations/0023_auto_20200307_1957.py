# Generated by Django 2.2.4 on 2020-03-07 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addentance', '0022_auto_20200307_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='detailed_attendance',
            field=models.ManyToManyField(blank=True, to='addentance.AttendanceTimestamp'),
        ),
    ]
