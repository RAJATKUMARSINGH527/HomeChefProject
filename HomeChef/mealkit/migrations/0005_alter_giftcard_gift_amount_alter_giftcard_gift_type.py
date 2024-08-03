# Generated by Django 5.0.6 on 2024-08-03 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealkit', '0004_rename_username_customer_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='gift_amount',
            field=models.IntegerField(choices=[(50, '$50'), (75, '$75'), (100, '$100'), (140, '$140'), (280, '$280')]),
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='gift_type',
            field=models.CharField(default='Meal', max_length=255),
        ),
    ]
