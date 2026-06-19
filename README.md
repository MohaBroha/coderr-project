# Coderr Backend

## Overview

Coderr is a Django REST Framework backend for a freelancer marketplace platform. The project provides APIs for managing user accounts, offers, orders, reviews, and profile information.

## Features

* User authentication and registration
* Profile management
* Offer management
* Search and filtering for offers
* Ordering and sorting
* RESTful API architecture
* Django REST Framework
* PostgreSQL/SQLite support
* Media file uploads

## Tech Stack

* Python
* Django
* Django REST Framework
* Django Filter
* SQLite (development)
* PostgreSQL (production)

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd coderr-project/backend
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Environment

Windows:

```bash
env\Scripts\activate
```

Linux/Mac:

```bash
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Start Development Server

```bash
python manage.py runserver
```

Server runs at:

```text
http://127.0.0.1:8000/
```

## API Structure

### Authentication

* Registration
* Login
* User Management

### Offers

* Create Offer
* Update Offer
* Delete Offer
* List Offers
* Search Offers
* Filter Offers
* Ordering Offers

### Profiles

* Profile Details
* Profile Updates

## Search and Filter

Available filters:

* user

Available search fields:

* title
* description

Available ordering fields:

* updated_at
* min_price

## Development Status

Current development focus:

* Offer API
* Filtering
* Search functionality
* Ordering functionality

## Author

Developer Academy Backend Project
Moha Broha
