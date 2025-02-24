import csv
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from kudos.models import Kudos, Organization

User = get_user_model()

class Command(BaseCommand):
    help = "Generate demo data for Kudos app"

    def handle(self, *args, **options):
        # Create or get organizations
        org_dict = {}
        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                org_name = row['organization']
                if org_name not in org_dict:
                    org, created = Organization.objects.get_or_create(name=org_name)
                    org_dict[org_name] = org
        
        # Read users from CSV and create them if they don't exist
        users = []
        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                org = org_dict[row['organization']]

                # Create user if not exists
                user, created = User.objects.get_or_create(
                    username=row['username'],
                    defaults={
                        "organization": org,
                        "remaining_kudos": int(row['remaining_kudos'])
                    }
                )
                user.set_password("password")
                user.save()

                # Reset remaining_kudos if user already exists
                if not created:
                    user.remaining_kudos = int(row['remaining_kudos'])
                    user.save()
                    self.stdout.write(self.style.WARNING(f"User {user.username} already exists, resetting remaining_kudos to {row['remaining_kudos']}."))

                users.append((user, row['message'], org))

        # Each user sends only one kudos to another user in the same organization
        for sender, custom_message, sender_org in users:
            if sender.remaining_kudos > 0:
                # Find receivers in the same organization
                receivers = [user[0] for user in users if user[0] != sender and user[2] == sender_org]

                if receivers:
                    receiver = receivers[0]  # Send kudos to the first available receiver
                    Kudos.objects.create(
                        sender=sender,
                        receiver=receiver,
                        message=custom_message,
                        created_at=now()
                    )

                    # Deduct only 1 kudos from the sender
                    sender.remaining_kudos -= 1
                    sender.save()

        self.stdout.write(self.style.SUCCESS("Demo data generated successfully."))
