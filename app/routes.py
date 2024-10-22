from flask import Blueprint, request, jsonify
from requests.auth import HTTPBasicAuth
import requests
import os
from datetime import datetime
import re  # Import regex for phone number validation
from . import db
from .models import Payment, Sale, Product
from flask_cors import CORS
import base64  # Added for password encoding
import logging  # Import logging for better debug messages

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define blueprint
bp = Blueprint('mpesa', __name__)
CORS(bp, resources={r"/api/mpesa/payment": {"origins": "http://localhost:5173", "supports_credentials": True}})

# M-Pesa credentials (use environment variables for security)
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
SHORTCODE = os.getenv('SHORTCODE')
PASSKEY = os.getenv('PASSKEY')
CALLBACK_URL = "https://mydomain.com/path"  # Change this to your actual callback URL

# Helper function to get access token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    logger.debug(f"Fetching access token from URL: {url}")
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    if response.status_code == 200:
        logger.debug("Access token fetched successfully.")
        return response.json()["access_token"]
    logger.error(f"Error fetching M-Pesa access token: {response.status_code}, {response.text}")
    raise Exception("Error fetching M-Pesa access token.")

# Helper function to validate and format phone number
def format_phone_number(phone_number):
    """Format and validate the phone number."""
    logger.debug(f"Formatting phone number: {phone_number}")
    if phone_number.startswith('07'):
        return '254' + phone_number[1:]
    elif phone_number.startswith('254'):
        return phone_number  # Already in international format
    else:
        logger.warning("Invalid phone number format provided.")
        return None  # Invalid format

# M-Pesa Payment Route
@bp.route('/api/mpesa/payment', methods=['POST', 'OPTIONS'])
def mpesa_payment():
    if request.method == 'OPTIONS':
        logger.debug("Handling preflight request.")
        return jsonify({"success": True}), 200  # Handle the preflight request

    data = request.get_json()
    logger.debug(f"Received payment data: {data}")
    
    phone_number = data.get('phone')
    amount = data.get('amount', 1)  # Fetch the amount from the request data

    # Validate phone number and amount
    if not phone_number or not amount:
        logger.warning("Phone number and amount are required.")
        return jsonify({"success": False, "message": "Phone number and amount are required"}), 400

    formatted_phone_number = format_phone_number(phone_number)
    if not formatted_phone_number:
        logger.warning("Invalid phone number format.")
        return jsonify({"success": False, "message": "Invalid phone number format"}), 400

    try:
        access_token = get_access_token()
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{SHORTCODE}{PASSKEY}{timestamp}".encode()).decode('utf-8')

        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": 254713961197,
            "PartyB": SHORTCODE,
            "PhoneNumber": 254713961197,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X"
        }

        # Log the payload for debugging
        logger.debug(f"Sending payment request with payload: {payload}")

        response = requests.post(url, json=payload, headers=headers)
        logger.debug(f"M-Pesa API response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            payment = Payment(amount=amount, phone_number=formatted_phone_number)
            db.session.add(payment)
            db.session.commit()
            logger.info(f"Payment recorded: {payment}")
            return jsonify({"success": True, "message": "Payment request sent", "data": response.json()}), 200
        else:
            logger.error(f"Payment request failed: {response.status_code}, {response.text}")
            return jsonify({"success": False, "message": "Payment request failed", "error": response.json()}), response.status_code

    except Exception as e:
        logger.exception("Error processing payment")
        return jsonify({"success": False, "message": str(e)}), 500

# Product Routes
@bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    logger.debug("Fetched products from database.")
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'category': p.category
    } for p in products]), 200

@bp.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    logger.debug(f"Adding new product: {data}")
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category']
    )
    db.session.add(new_product)
    db.session.commit()
    logger.info("New product added successfully!")
    return jsonify({'message': 'Product added successfully!'}), 201

# Sales Routes
@bp.route('/api/sales', methods=['POST'])
def add_sale():
    data = request.get_json()
    logger.debug(f"Adding new sale: {data}")
    new_sale = Sale(
        product_id=data['product_id'],
        time=datetime.now(),
        quantity=data['quantity']
    )
    db.session.add(new_sale)
    db.session.commit()
    logger.info("New sale recorded.")
    return jsonify({'message': 'Sale added!'}), 201


