# Generated by Django 2.2 on 2021-06-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0008_auto_20210531_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='leitura',
            name='paginas_restante',
            field=models.IntegerField(default=0),
        ),
    ]