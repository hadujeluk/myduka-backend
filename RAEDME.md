# My Duka App

My Duka App is a web application built using Flask. It allows users to manage products, sales, and payments with integration to M-Pesa for handling payments. The app uses SQLAlchemy for database management, Flask-Migrate for database migrations, and supports CORS to interact with external front-end applications.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Products](#products)
  - [Sales](#sales)
  - [M-Pesa Payments](#m-pesa-payments)
- [Contributing](#contributing)
- [License](#license)

## Features

- Manage products: Add, view, and manage product listings.
- Track sales: Record sales transactions and maintain records.
- Payment processing: Integration with M-Pesa for seamless payments.
- CORS enabled for interaction with external front-end applications.

## Technologies Used

- **Flask**: A web framework for building server-side applications.
- **SQLAlchemy**: A toolkit for working with databases in Python.
- **Flask-Migrate**: For handling database migrations.
- **Flask-CORS**: To enable CORS and allow cross-origin requests.
- **M-Pesa API**: Integration for handling mobile payments.
- **SQLite**: Database for storing product, sales, and payment information.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- pip (Python package installer)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Tonykanyi/MyDukaBackend
    cd my-duka-app
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    flask db upgrade
    ```

### Environment Variables

Create a `.env` file in the root directory and set the following environment variables:

```bash
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
SHORTCODE=your_shortcode
PASSKEY=your_passkey
SQLALCHEMY_DATABASE_URI=sqlite:///my_duka.db
CALLBACK_URL=https://yourdomain.com/path
Replace your_consumer_key, your_consumer_secret, your_shortcode, your_passkey, and https://yourdomain.com/path with your actual values.

Running the Application
Start the Flask application:

bash
Copy code
flask run
The application will run on http://0.0.0.0:5000.

API Endpoints
Products
GET /api/products - Fetch all products
POST /api/products - Add a new product
Example of adding a product:

json
Copy code
{
  "name": "Product Name",
  "description": "Product Description",
  "price": 100.0,
  "category": "Electronics"
}
Sales
POST /api/sales - Add a new sale
Example of adding a sale:

json
Copy code
{
  "product_id": 1,
  "quantity": 2
}
M-Pesa Payments
POST /api/mpesa/payment - Initiate an M-Pesa payment request
Example of initiating a payment:

json
Copy code
{
  "phone": "0712345678",
  "amount": 500
}
Contributing
We welcome contributions! Please fork the repository and create a pull request with your feature or bug fix.

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes and commit them (git commit -am 'Add some feature').
Push the changes to your branch (git push origin feature/your-feature-name).
Create a new Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

 `"https://github.com/Tonykanyi/MyDukaBackend"` and environment variable values with actual information relevant to your setup. Let me know if you need any additional sections or adjustments!





