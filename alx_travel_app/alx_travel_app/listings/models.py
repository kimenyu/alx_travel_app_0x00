from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Listing Model
class Listing(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(help_text="Comma-separated list of amenities.")
    availability_start = models.DateField()
    availability_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.availability_start >= self.availability_end:
            raise ValidationError(_('Availability start date must be before end date.'))

# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]

    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking by {self.guest} for {self.listing}"

    def clean(self):
        if self.check_in_date >= self.check_out_date:
            raise ValidationError(_('Check-in date must be before check-out date.'))

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            listing=self.listing,
            status__in=['pending', 'confirmed'],
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date
        )
        if overlapping_bookings.exists():
            raise ValidationError(_('This property is already booked for the selected dates.'))

# Review Model
class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(help_text=_('Rating between 1 and 5'))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.booking.listing} by {self.reviewer}"

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError(_('Rating must be between 1 and 5.'))

