# Generated by Django 4.1 on 2023-09-01 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0014_cart_owner_cart_session_id_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='f00b5bcf', max_length=10, unique=True),
        ),
    ]