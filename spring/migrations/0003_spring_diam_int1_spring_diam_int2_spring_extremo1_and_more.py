# Generated by Django 4.1.4 on 2023-03-07 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spring', '0002_remove_spring_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='spring',
            name='diam_int1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='spring',
            name='diam_int2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='spring',
            name='extremo1',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='spring',
            name='extremo2',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='spring',
            name='grado',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='spring',
            name='vuelta_red1',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='spring',
            name='vuelta_red2',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
    ]
