# ALX Travel App 0x00

This is a Django-based application that facilitates the management of travel listings, bookings, and reviews. The app allows users to browse listings, make bookings, and leave reviews for their stays.

## Project Overview

The project includes the following features:
- **User Management**: User registration, login, and authentication.
- **Listing Management**: Manage travel listings with details like name, description, price, and location.
- **Booking Management**: Users can book listings, specify start and end dates, and calculate the total price.
- **Review System**: Users can leave ratings and comments on listings.

## Features

### 1. User Management:
- Users can sign up, log in, and manage their profile.
- Role-based authentication (admin, user) for better access control.

### 2. Listing Management:
- Admins can create, update, and delete listings.
- Each listing contains information such as the host, description, location, and price.

### 3. Booking Management:
- Users can make bookings for the listings with specified start and end dates.
- Total price is calculated based on the price per night and duration of the stay.

### 4. Review System:
- Users can leave reviews for each listing they have stayed at.
- Reviews include ratings (1-5) and comments.

## Requirements

Before running the application, ensure you have the following installed:
- Python 3.x
- Django
- Django REST Framework
- PostgreSQL (for database)
- Faker (for generating fake data)

To install dependencies, run the following command:
```bash
pip install -r requirements.txt
