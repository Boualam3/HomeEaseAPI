# Generated by Django 5.1 on 2024-09-02 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_remove_member_user_profile_delete_address_and_more"),
        ("properties", "0005_property_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="host",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="collections",
                to="core.profile",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="property",
            name="host",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties",
                to="core.profile",
            ),
            preserve_default=False,
        ),
    ]
