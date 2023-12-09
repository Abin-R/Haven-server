from django.core.management.base import BaseCommand
from django.utils import timezone
from subscription.models import SubscriptionPayment, SubcribedUsers
from django.contrib.auth import logout

class Command(BaseCommand):
    help = 'Update subscriptions and log out users if expired'

    def handle(self, *args, **options):
        # Get all SubscriptionPayment instances
        subscriptions = SubscriptionPayment.objects.all()
        print(subscriptions)

        for subscription in subscriptions:
            # Check if the subscription is expired
            if subscription.is_expired():
                # Update SubcribedUsers boolean fields
                subscribed_user = SubcribedUsers.objects.get(user=subscription.user)
                subscribed_user.is_premium = False
                subscribed_user.is_super = False
                subscribed_user.save()

                # Log out the user
                logout(subscription.user)

                # Print a message for logging purposes
                self.stdout.write(self.style.SUCCESS(f'Updated subscription for user {subscription.user.username}'))

        self.stdout.write(self.style.SUCCESS('Subscription update complete'))
