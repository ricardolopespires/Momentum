# Generated by Django 2.2 on 2021-05-31 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actor', '0002_actor_movies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
