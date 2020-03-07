# Generated by Django 2.2.4 on 2020-03-03 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addentance', '0015_auto_20200229_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceTimestamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField()),
                ('timestamp', models.DateTimeField()),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addentance.Student')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addentance.Subject')),
            ],
        ),
    ]