# Generated by Django 5.1a1 on 2024-08-07 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0002_add_groups"),
    ]

    operations = [
        migrations.AddField(
            model_name="approveddrug",
            name="is_controlled",
            field=models.BooleanField(default=False),
        ),
    ]