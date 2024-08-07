# Generated by Django 5.0.6 on 2024-07-31 19:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0011_remove_listing_winner"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="winner_listing",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
