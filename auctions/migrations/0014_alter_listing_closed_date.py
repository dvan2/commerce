# Generated by Django 5.0.6 on 2024-08-02 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0013_alter_listing_closed_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="closed_date",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
