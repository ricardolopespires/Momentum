# Generated by Django 2.2 on 2021-05-30 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0005_auto_20210530_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='total_horas',
            field=models.CharField(default='00:00:00', max_length=150),
        ),
    ]
