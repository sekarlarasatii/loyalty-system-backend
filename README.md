# Loyalty Points and Digital Payment System

This project is a backend API (RESTful) for a loyalty points system integrated with a simulated digital payment system. The system includes user management, points management, payment simulation, data warehousing, background tasks, and monitoring.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `.env.example` file and update the environment variables as needed.

5. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Start the Celery worker:
   ```bash
   celery -A loyalty_system worker --loglevel=info
   ```

9. Start the Flower monitoring tool:
   ```bash
   celery -A loyalty_system flower
   ```

## Usage Instructions

1. Register a new user by sending a POST request to `/api/users/register/` with the following JSON payload:
   ```json
   {
     "email": "user@example.com",
     "password": "password123",
     "name": "John Doe"
   }
   ```

2. Log in by sending a POST request to `/api/users/login/` with the following JSON payload:
   ```json
   {
     "email": "user@example.com",
     "password": "password123"
   }
   ```

3. Use the obtained JWT access token to authenticate subsequent requests by including it in the `Authorization` header:
   ```http
   Authorization: Bearer <access_token>
   ```

4. View and update the user's profile by sending a GET or PUT request to `/api/users/profile/`.

5. Redeem points for a voucher by sending a POST request to `/api/points/redeem/` with the following JSON payload:
   ```json
   {
     "voucher_id": 1
   }
   ```

6. Simulate a payment by sending a POST request to `/api/transactions/pay/` with the following JSON payload:
   ```json
   {
     "amount": 100000,
     "payment_method": "Dummy Credit Card"
   }
   ```

## API Documentation

The complete API documentation is available at `/swagger/`.

