# Generated by Django 5.1.4 on 2024-12-20 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_remove_history_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraper.category'),
        ),
    ]
