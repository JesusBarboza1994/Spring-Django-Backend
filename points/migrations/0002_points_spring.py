# Generated by Django 4.1.4 on 2022-12-29 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spring', '0002_remove_spring_point'),
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='points',
            name='spring',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='spring.spring'),
        ),
    ]
