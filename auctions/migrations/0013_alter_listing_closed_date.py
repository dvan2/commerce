# Generated by Django 5.0.6 on 2024-08-01 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0012_listing_winner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="closed_date",
            field=models.DateTimeField(null=True),
        ),
    ]