# Generated by Django 4.2.6 on 2023-10-25 20:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0007_maintenance_requires_items"),
    ]

    operations = [
        migrations.RenameField(
            model_name="maintenance",
            old_name="item",
            new_name="target_item",
        ),
    ]
