# BOL Management System

A Django-based web application for managing Bill of Lading inventory, converted from your existing Google Sheets/Apps Script system. This application is designed for Cincinnati Barge & Rail Terminal, LLC.

## Features

- **Master Data Management**: Items, Sizes, Suppliers, Customers, Carriers, Trucks, and Locations
- **Batch Entry**: Track inventory batches with barcodes, quantities, and status
- **User-friendly Interface**: Matches your existing SPA design with Bootstrap styling
- **API Endpoints**: RESTful API for AJAX operations
- **Admin Interface**: Django admin for advanced management
- **Reports**: BOL generation and inventory reports

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: Bootstrap 5, jQuery, vanilla JavaScript
- **Deployment**: Render (with WhiteNoise for static files)
- **Authentication**: Django's built-in user system

## Local Development Setup

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd bol_management
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Create sample data** (optional):
   ```bash
   python manage.py create_sample_data
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the application**:
   - Main application: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/

## Deployment to Render

### Prerequisites

- Render account
- GitHub repository with your code

### Deployment Steps

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**:
   The `render.yaml` file automatically sets up:
   - Database connection
   - Secret key generation
   - Production settings

4. **Deploy**:
   - Render will automatically build and deploy your app
   - The build process runs `build.sh` which:
     - Installs dependencies
     - Collects static files
     - Runs migrations
     - Creates a default admin user

5. **Access Your App**:
   - Your app will be available at: `https://bol-management.onrender.com`
   - Admin login: username `admin`, password `admin123` (change this!)

## Project Structure

```
bol_management/
├── bol_management/          # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main settings file
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── inventory/             # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # App URLs
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   ├── templates/         # HTML templates
│   │   └── inventory/
│   │       ├── base.html
│   │       ├── main_menu.html
│   │       └── ...
│   ├── management/        # Custom commands
│   │   └── commands/
│   │       └── create_sample_data.py
│   └── migrations/        # Database migrations
├── requirements.txt       # Python dependencies
├── build.sh              # Render build script
├── render.yaml           # Render configuration
├── manage.py             # Django management script
└── README.md            # This file
```

## API Endpoints

The application provides RESTful API endpoints that match your existing Google Scripts functions:

- `GET /api/items/` - Get all items
- `POST /api/items/` - Add new item
- `PUT /api/items/` - Update item
- `DELETE /api/items/` - Delete item

Similar endpoints exist for: sizes, suppliers, customers, carriers, trucks, locations, and batches.

## Models Overview

### Core Models
- **Item**: Product definitions (item code, name, standard bag weight)
- **Size**: Size specifications (-16, 3x6, etc.)
- **Supplier**: Supplier information with BOL prefixes
- **Customer**: Customer information
- **Carrier**: Trucking companies
- **Truck**: Individual trucks per carrier
- **Location**: Customer delivery locations
- **Batch**: Inventory batches with barcodes and quantities

### Operational Models
- **BOL**: Bills of Lading
- **BOLItem**: Individual items on a BOL

## Management Commands

### Create Sample Data
```bash
python manage.py create_sample_data
```
Creates sample data for testing and demonstration.

### Clear and Recreate Data
```bash
python manage.py create_sample_data --clear
```
Clears existing data and creates fresh sample data.

## Configuration

### Environment Variables

- `SECRET_KEY`: Django secret key (auto-generated on Render)
- `DEBUG`: Set to `True` for development, `False` for production
- `DATABASE_URL`: Database connection string (auto-set on Render)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database

- **Development**: Uses SQLite by default
- **Production**: Uses PostgreSQL on Render

## Security Features

- CSRF protection enabled
- SQL injection protection via Django ORM
- XSS protection via template auto-escaping
- Secure headers in production
- Static file serving via WhiteNoise

## Customization

### Adding New Fields
1. Update the model in `inventory/models.py`
2. Create and run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Update forms in `inventory/forms.py`
4. Update templates as needed

### Styling Changes
- Modify the CSS in `inventory/templates/inventory/base.html`
- The design maintains your existing gradient theme and card-based layout

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check your `DATABASE_URL` environment variable
   - Ensure PostgreSQL is running (for local PostgreSQL setup)

2. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` settings

3. **Migration Issues**:
   - Delete migration files (keep `__init__.py`)
   - Run `python manage.py makemigrations`
   - Run `python manage.py migrate`

### Logs and Debugging

- **Local Development**: Check the console output
- **Render**: View logs in the Render dashboard
- **Django Debug**: Set `DEBUG=True` in development only

## Support

For issues or questions about this Django conversion:
1. Check the Django documentation
2. Review the code comments
3. Test with sample data using the management command

## Migration from Google Sheets

Your existing Google Sheets data can be migrated by:
1. Exporting data to CSV format
2. Creating a custom management command to import CSV data
3. Mapping the spreadsheet columns to Django model fields

The API endpoints maintain compatibility with your existing JavaScript code structure.