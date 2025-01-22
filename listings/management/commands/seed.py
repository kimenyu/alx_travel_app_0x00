from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample Listing data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Optional: Clear existing data
        Listing.objects.all().delete()

        locations = ['Paris', 'New York', 'Tokyo', 'Sydney', 'Cape Town', 'Rome', 'Barcelona', 'Dubai', 'Singapore', 'London']
        
        # Create sample users (you could modify this as needed, or create more users)
        users = []
        for _ in range(5):
            users.append(User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123"
            ))

        # Create sample listings
        for _ in range(20):
            name = fake.sentence(nb_words=4)  # Use 'name' as per the model
            description = fake.paragraph(nb_sentences=5)
            location = random.choice(locations)
            price_per_night = round(random.uniform(50, 500), 2)
            available_from = fake.date_between(start_date='today', end_date='+30d')
            available_to = available_from + timedelta(days=random.randint(5, 30))

            # Assign a random user as the host for each listing
            host = random.choice(users)

            listing = Listing.objects.create(
                host_id=host,  # Ensure host is a User object
                name=name,
                description=description,
                location=location,
                price_per_night=price_per_night,
                created_at=fake.date_this_year(),
                updated_at=fake.date_this_year(),
            )

            self.stdout.write(self.style.SUCCESS(f'Created listing: {listing.name}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))
