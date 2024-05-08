# Generated by Django 5.0.3 on 2024-05-08 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("policy", "0002_initial"),
        ("product_portfolio", "0004_alter_scancodeproject_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usagepolicy",
            name="associated_product_relation_status",
            field=models.ForeignKey(
                blank=True,
                help_text="An associated product relation status enables you to specify the product relation status to use automatically when a component or package with an assigned usage policy is added to a product, overriding the general default defined in the product relation status table.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product_portfolio.productrelationstatus",
            ),
        ),
    ]
