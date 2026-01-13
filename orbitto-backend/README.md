# Orbitto ERP Backend

A comprehensive Python-based ERP (Enterprise Resource Planning) system backend built with Flask and SQLAlchemy.

## Architecture

### Directory Structure
```
orbitto-backend/
├── app/
│   ├── models/              # SQLAlchemy database models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── customer.py
│   │   ├── inventory.py
│   │   └── __init__.py
│   ├── routes/              # API route blueprints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── customers.py
│   │   ├── inventory.py
│   │   └── __init__.py
│   ├── middleware/          # Custom middleware
│   ├── services/            # Business logic services
│   ├── schemas/             # Request/Response validation schemas
│   ├── utils/               # Utility functions
│   └── __init__.py          # App factory
├── migrations/              # Database migrations
├── tests/                   # Unit and integration tests
├── config.py                # Configuration management
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables example
└── README.md
```

## Features

- **Authentication**: JWT-based user authentication and authorization
- **User Management**: Create, read, update, delete users with role-based access
- **Product Management**: Manage products with SKU tracking and pricing
- **Order Management**: Create and track customer orders with order items
- **Customer Management**: Store and manage customer information
- **Inventory Management**: Track stock levels, reorder points, and low-stock alerts
- **Security**: Password hashing with Werkzeug, JWT token authentication
- **Error Handling**: Consistent error responses across the API
- **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- MySQL/PostgreSQL (or SQLite for development)

## Installation

### 1. Clone and Setup Virtual Environment

```bash
cd orbitto-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
```

### 4. Initialize Database

```bash
# Create database tables
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

# Or using the CLI command
python run.py init_db
```

## Running the Application

### Development Mode

```bash
python run.py
```

The server will start on `http://localhost:5000`

### Using Flask CLI

```bash
# Set Flask app
export FLASK_APP=run.py
export FLASK_ENV=development

# Run development server
flask run

# Initialize database
flask init_db

# Drop database
flask drop_db
```

## API Endpoints

### Health Check
- `GET /api/health` - Server health status

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login

### Users (Requires JWT)
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get user by ID
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user (soft delete)

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get product by ID
- `POST /api/products` - Create product (Requires JWT)
- `PUT /api/products/<id>` - Update product (Requires JWT)
- `DELETE /api/products/<id>` - Delete product (Requires JWT)

### Customers (Requires JWT)
- `GET /api/customers` - Get all customers
- `GET /api/customers/<id>` - Get customer by ID
- `POST /api/customers` - Create customer
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Orders (Requires JWT)
- `GET /api/orders` - Get all orders
- `GET /api/orders/<id>` - Get order by ID
- `POST /api/orders` - Create order
- `PUT /api/orders/<id>` - Update order

### Inventory (Requires JWT)
- `GET /api/inventory` - Get all inventory
- `GET /api/inventory/<id>` - Get inventory item
- `PUT /api/inventory/<id>` - Update inventory
- `GET /api/inventory/low-stock` - Get low stock items

## Environment Variables

```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=mysql+pymysql://user:password@localhost/orbitto
SQLALCHEMY_TRACK_MODIFICATIONS=False
CORS_ORIGIN=http://localhost:3000
```

## Database Models

### User
- id, email (unique), password_hash
- first_name, last_name
- role: admin, manager, user
- is_active, timestamps

### Product
- id, name, description
- sku (unique), price, category
- quantity, reorder_level, supplier
- is_active, timestamps

### Customer
- id, name, email (unique)
- phone, address, city, state
- postal_code, country
- is_active, timestamps

### Order
- id, order_number (unique)
- customer_id (FK)
- total_amount, status
- order_date, delivery_date
- notes, timestamps

### OrderItem
- id, order_id (FK), product_id (FK)
- quantity, unit_price, total

### Inventory
- id, product_id (FK, unique)
- quantity_on_hand, quantity_reserved
- quantity_available
- reorder_point, reorder_quantity
- last_counted, timestamps

## Authentication

All endpoints that require JWT authentication expect the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Getting a Token

1. Register or Login:
```bash
POST /api/auth/register
POST /api/auth/login
```

2. Use the returned token in subsequent requests

## Error Responses

Standard error response format:

```json
{
  "error": "Error message"
}
```

HTTP Status Codes:
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

## Development

### Code Structure Best Practices

- Keep business logic in `/services`
- Use blueprints for route organization
- Implement validation in schemas
- Middleware for cross-cutting concerns
- Use SQLAlchemy ORM patterns

### Database Migrations

Using Flask-Migrate for schema changes:

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Revert migration
flask db downgrade
```

### Testing

```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=app
```

## Future Enhancements

- [ ] Advanced reporting and analytics
- [ ] Email notifications
- [ ] Payment gateway integration
- [ ] Advanced inventory management (warehouses, transfers)
- [ ] Batch operations and bulk imports
- [ ] API rate limiting
- [ ] Comprehensive logging
- [ ] WebSocket support for real-time updates
- [ ] GraphQL API
- [ ] Docker containerization

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check MySQL/PostgreSQL is running
- Ensure database user has proper permissions

### Virtual Environment Issues
```bash
# Deactivate current venv
deactivate

# Remove venv
rm -rf venv

# Recreate and activate
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## License

MIT
