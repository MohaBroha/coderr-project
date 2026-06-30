# Coderr Backend

## Overview

Coderr is a Django REST Framework backend for a freelancer marketplace platform. The project provides REST APIs for user authentication, profiles, offers, orders, reviews, and platform statistics.

## Features

* User registration and authentication
* Profile management
* Offer management
* Order management
* Review system
* Search, filtering and ordering
* RESTful API architecture
* Token authentication
* Media file support

## Tech Stack

* Python
* Django
* Django REST Framework
* Django Filter
* SQLite (development)
* PostgreSQL (production)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MohaBroha/coderr-project.git
```

### 2. Navigate to the backend directory

```bash
cd coderr-project
cd backend
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 5. Install the dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Copy the example environment file:

**Linux / macOS**

```bash
cp .env.example .env
```

**Windows**

```powershell
copy .env.example .env
```

Then adjust the values in the `.env` file if necessary.

Example:

```env
SECRET_KEY=your_secret_key_here
```

### 7. Apply the database migrations

```bash
python manage.py migrate
```

### 8. Start the development server

```bash
python manage.py runserver
```

The development server will be available at:

```text
http://127.0.0.1:8000/
```

## Running Tests

Run all tests:

```bash
python manage.py test --settings=core.test_settings
```

Run tests for a specific app:

```bash
python manage.py test reviews_app.tests.test_views --settings=core.test_settings
```

Replace `reviews_app.tests.test_views` with the desired test module if you want to execute a different test suite.

## API Endpoints

* Authentication

  * Registration
  * Login

* Profiles

  * Profile Details
  * Business Profiles
  * Customer Profiles

* Offers

  * List Offers
  * Offer Details
  * Create Offer
  * Update Offer
  * Delete Offer

* Orders

  * List Orders
  * Order Details
  * Active Order Count
  * Completed Order Count

* Reviews

  * List Reviews
  * Create Review
  * Update Review
  * Delete Review

* Base Information

  * Platform Statistics

## Search, Filter and Ordering

### Offers

**Search**

* title
* description

**Filter**

* creator_id
* min_price
* max_delivery_time

**Ordering**

* updated_at
* min_price

## Development

This project was built with Django REST Framework following a modular app structure and REST API best practices.

## Author

Moha Broha