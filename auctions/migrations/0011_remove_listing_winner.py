# Generated by Django 5.0.6 on 2024-07-31 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_alter_bidding_listing"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="winner",
        ),
    ]