# Generated by Django 4.1 on 2023-06-15 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_alter_customerreview_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='61ee8152', max_length=10, unique=True),
        ),
    ]
