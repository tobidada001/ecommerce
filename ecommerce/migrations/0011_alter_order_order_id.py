# Generated by Django 4.2.1 on 2023-06-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_remove_cart_owner_remove_order_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='daa8ffbe', max_length=10, unique=True),
        ),
    ]
