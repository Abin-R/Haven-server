# Generated by Django 4.2.7 on 2023-11-29 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_booking_ticket_transaction_event_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='ticket_count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
