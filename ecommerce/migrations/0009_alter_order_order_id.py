# Generated by Django 4.1 on 2023-06-15 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='ebbf6a6f', max_length=10, unique=True),
        ),
    ]
