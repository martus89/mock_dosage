# Generated by Django 5.1a1 on 2024-08-15 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0004_rename_quantity_product_packaging_quantity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approveddrug",
            name="extra_info",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="drugformchoice",
            name="extra_info",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="extra_info",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="storage",
            name="extra_info",
            field=models.TextField(blank=True, default="", null=True),
        ),
    ]
