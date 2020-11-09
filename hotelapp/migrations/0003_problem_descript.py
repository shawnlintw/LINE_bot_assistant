# Generated by Django 3.0.4 on 2020-09-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0002_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='problem_descript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='0', max_length=50)),
                ('locate', models.CharField(max_length=20)),
                ('equipment', models.CharField(max_length=50)),
                ('equipment_location', models.CharField(max_length=10)),
                ('problem_descript', models.CharField(max_length=200)),
            ],
        ),
    ]