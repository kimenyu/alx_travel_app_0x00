import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing
from faker import Faker

class Command(BaseCommand):
    help = 'Seed the database with sample listings data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create sample hosts
        if User.objects.filter(is_staff=False).count() < 5:
            self.stdout.write('Creating sample hosts...')
            for _ in range(5):
                User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password='password123'
                )

        hosts = User.objects.filter(is_staff=False)

        # Create sample listings
        self.stdout.write('Creating sample listings...')
        for _ in range(20):
            host = random.choice(hosts)
            title = fake.sentence(nb_words=4)
            description = fake.paragraph(nb_sentences=5)
            location = fake.city()
            price_per_night = round(random.uniform(50, 500), 2)
            amenities = ', '.join(fake.words(nb=5))
            availability_start = fake.date_this_year(before_today=False, after_today=True)
            availability_end = fake.date_this_year(before_today=False, after_today=True)

            # Ensure the availability dates are valid
            if availability_start > availability_end:
                availability_start, availability_end = availability_end, availability_start

            Listing.objects.create(
                host=host,
                title=title,
                description=description,
                location=location,
                price_per_night=price_per_night,
                amenities=amenities,
                availability_start=availability_start,
                availability_end=availability_end
            )

        self.stdout.write(self.style.SUCCESS('Database seeded with sample listings data!'))