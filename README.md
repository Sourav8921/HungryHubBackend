# HungryHub - Food Delivery App Backend

This is the backend repository for **HungryHub**, a food delivery application built with Python Django, providing a robust RESTful API for managing restaurant listings, menu items, orders, user authentication, payment processing, and more. This repository includes models, views, and APIs that power the frontend built with React Native.

## Features

### 1. User Authentication & Authorization
- **JWT-based Authentication**: Uses `drf-simplejwt` to provide secure JSON Web Token (JWT) authentication.
- **Token Refresh**: Uses Axios interceptors for token refreshing to maintain active sessions.
- **AsyncStorage Integration**: Manages token storage and persistence in the frontend.

### 2. Restaurant & Menu Management
- **Restaurant Listings**: Customizable models.
- **Menu Browsing**: Provides categorized menu items with support for filtering restaurants using menu item name.

### 3. Cart Management
- **Redux Toolkit**: Manages cart state effectively in the frontend.

### 4. Payment Processing
- **Stripe Integration**: Handles card payments, with backend verification before order creation.
- **Cash on Delivery (COD)**: Available as a payment option without verification.

### 5. Order Processing & Tracking
- **Order Management**: Provides real-time order status updates and supports order cancellation.
- **Order History**: Allows users to view past orders.

### 6. Address Management
- **CRUD Operations**: Allows users to add, update, delete, and label addresses.

### 7. Search & Filter
- **Restaurant Search**: Filters restaurants based on food items.
  
### 8. Profile Management
- **User Information Management**: Allows users to update profile details via PATCH requests.

## Tech Stack

- **Backend Framework**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Media Storage**: AWS S3 for user-uploaded images
- **Payment Gateway**: Stripe
- **Authentication**: JWT, drf-simplejwt

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database
- AWS S3 bucket (for media files)
- Stripe API keys

### Setup Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sourav8921/HungryHubBackend.git
   cd HungryHubBackend
   
2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt

3. Set up environment variables: Create a .env file in the root directory and configure the following:
    ```bash
    SECRET_KEY=your_secret_key
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=your_db_host
    DATABASE_PORT=your_db_port
    STRIPE_SECRET_KEY=your_stripe_secret_key
    AWS_ACCESS_KEY_ID=your_aws_access_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret_key
    AWS_STORAGE_BUCKET_NAME=your_bucket_name
    DEBUG=True ## change to False for production

4. Run migrations:

    ```bash
    python manage.py migrate

5. Create a superuser (for admin access):

    ```bash
    python manage.py createsuperuser
   
6. Start the server:
    ```bash
    python manage.py runserver
The server will start at http://127.0.0.1:8000.

## Contributions
Contributions are welcome! Please fork this repository, create a new branch for your feature or bug fix, and submit a pull request with detailed information.