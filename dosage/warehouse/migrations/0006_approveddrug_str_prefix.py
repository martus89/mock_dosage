# Generated by Django 5.1a1 on 2024-08-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0005_alter_approveddrug_extra_info_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="approveddrug",
            name="str_prefix",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
