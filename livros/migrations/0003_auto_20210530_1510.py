# Generated by Django 2.2 on 2021-05-30 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0002_leitura_pre_requisito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='Average_Count',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]