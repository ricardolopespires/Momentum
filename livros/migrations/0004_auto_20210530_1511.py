# Generated by Django 2.2 on 2021-05-30 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0003_auto_20210530_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='Average_Count',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]
