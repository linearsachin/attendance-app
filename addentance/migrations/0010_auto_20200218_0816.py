# Generated by Django 3.0.3 on 2020-02-18 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addentance', '0009_attendance_class_s'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='class_s',
        ),
        migrations.AddField(
            model_name='student',
            name='class_s',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addentance.Class'),
        ),
    ]
