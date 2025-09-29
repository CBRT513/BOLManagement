from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models import (
    Item, Size, Supplier, Customer, Carrier, Truck, Location, Batch
)
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Create sample data for BOL Management System'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating samples',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            with transaction.atomic():
                Batch.objects.all().delete()
                Location.objects.all().delete()
                Truck.objects.all().delete()
                Carrier.objects.all().delete()
                Customer.objects.all().delete()
                Supplier.objects.all().delete()
                Size.objects.all().delete()
                Item.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared successfully'))

        self.stdout.write('Creating sample data...')
        
        with transaction.atomic():
            # Create Items
            items_data = [
                {'item_code': 'BX75', 'item_name': 'Bauxite 75', 'weight': 1.5},
                {'item_code': 'BX50', 'item_name': 'Bauxite 50', 'weight': 1.2},
                {'item_code': 'AL100', 'item_name': 'Alumina 100', 'weight': 1.8},
                {'item_code': 'CL80', 'item_name': 'Clay 80', 'weight': 1.3},
                {'item_code': 'SA60', 'item_name': 'Sand 60', 'weight': 1.0},
            ]
            
            items = []
            for item_data in items_data:
                item, created = Item.objects.get_or_create(
                    item_code=item_data['item_code'],
                    defaults={
                        'item_name': item_data['item_name'],
                        'standard_bag_weight': item_data['weight']
                    }
                )
                items.append(item)
                if created:
                    self.stdout.write(f'Created item: {item.item_code}')

            # Create Sizes
            size_labels = ['-16', '3x6', '6x16', '-8', '12x20', '8x12']
            sizes = []
            for label in size_labels:
                size, created = Size.objects.get_or_create(size_label=label)
                sizes.append(size)
                if created:
                    self.stdout.write(f'Created size: {size.size_label}')

            # Create Suppliers
            suppliers_data = [
                {'name': 'YAS Industries', 'prefix': 'YAS', 'next_bol': 1001},
                {'name': 'Bauxite Corp', 'prefix': 'BXC', 'next_bol': 2001},
                {'name': 'Mining Solutions LLC', 'prefix': 'MSL', 'next_bol': 3001},
                {'name': 'Industrial Materials Co', 'prefix': 'IMC', 'next_bol': 4001},
            ]
            
            suppliers = []
            for sup_data in suppliers_data:
                supplier, created = Supplier.objects.get_or_create(
                    supplier_name=sup_data['name'],
                    defaults={
                        'bol_prefix': sup_data['prefix'],
                        'next_bol_no': sup_data['next_bol']
                    }
                )
                suppliers.append(supplier)
                if created:
                    self.stdout.write(f'Created supplier: {supplier.supplier_name}')

            # Create Customers
            customers_data = [
                {'name': 'Steel Works Inc', 'code': 'SWI'},
                {'name': 'Construction Materials LLC', 'code': 'CML'},
                {'name': 'Manufacturing Corp', 'code': 'MFC'},
                {'name': 'Industrial Supply Co', 'code': 'ISC'},
            ]
            
            customers = []
            for cust_data in customers_data:
                customer, created = Customer.objects.get_or_create(
                    customer_name=cust_data['name'],
                    defaults={'customer_code': cust_data['code']}
                )
                customers.append(customer)
                if created:
                    self.stdout.write(f'Created customer: {customer.customer_name}')

            # Create Carriers
            carriers_data = [
                {'name': 'ABC Trucking', 'code': 'ABC'},
                {'name': 'XYZ Transport', 'code': 'XYZ'},
                {'name': 'Fast Freight LLC', 'code': 'FFL'},
                {'name': 'Reliable Carriers', 'code': 'RCR'},
            ]
            
            carriers = []
            for carr_data in carriers_data:
                carrier, created = Carrier.objects.get_or_create(
                    carrier_name=carr_data['name'],
                    defaults={'carrier_code': carr_data['code']}
                )
                carriers.append(carrier)
                if created:
                    self.stdout.write(f'Created carrier: {carrier.carrier_name}')

            # Create Trucks
            for carrier in carriers:
                for i in range(1, 4):  # 3 trucks per carrier
                    truck_number = f"{i:03d}"
                    trailer_number = f"T{i:03d}" if i % 2 == 0 else ""
                    
                    truck, created = Truck.objects.get_or_create(
                        carrier=carrier,
                        truck_number=truck_number,
                        defaults={'trailer_number': trailer_number}
                    )
                    if created:
                        self.stdout.write(f'Created truck: {truck}')

            # Create Locations
            for customer in customers:
                for i in range(1, 3):  # 2 locations per customer
                    location_name = f"Plant {i}"
                    
                    location, created = Location.objects.get_or_create(
                        customer=customer,
                        location_name=location_name,
                        defaults={
                            'location_address': f"{i}00 Industrial Way",
                            'location_city': 'Cincinnati',
                            'location_state': 'OH',
                            'location_zip': f'4520{i}'
                        }
                    )
                    if created:
                        self.stdout.write(f'Created location: {location}')

            # Create Sample Batches
            for i in range(20):
                item = random.choice(items)
                size = random.choice(sizes)
                supplier = random.choice(suppliers)
                
                # Generate a receipt date within the last 60 days
                receipt_date = date.today() - timedelta(days=random.randint(0, 60))
                
                batch_data = {
                    'item': item,
                    'size': size,
                    'supplier': supplier,
                    'lot_number': f'L{1000 + i}',
                    'barge': f'BARGE{i % 5 + 1}',
                    'starting_quantity': random.randint(100, 1000),
                    'receipt_date': receipt_date,
                    'status': random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'DEPLETED']),  # More active than depleted
                }
                
                # Auto-generate barcode will happen in model save()
                batch = Batch.objects.create(**batch_data)
                
                # Randomize current quantity for some variety
                if batch.status == 'ACTIVE':
                    batch.current_quantity = random.randint(
                        batch.starting_quantity // 4,
                        batch.starting_quantity
                    )
                else:
                    batch.current_quantity = 0
                batch.save()
                
                if i < 5:  # Only show first 5 to avoid spam
                    self.stdout.write(f'Created batch: {batch.barcode}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {Item.objects.count()} Items\n'
                f'- {Size.objects.count()} Sizes\n'
                f'- {Supplier.objects.count()} Suppliers\n'
                f'- {Customer.objects.count()} Customers\n'
                f'- {Carrier.objects.count()} Carriers\n'
                f'- {Truck.objects.count()} Trucks\n'
                f'- {Location.objects.count()} Locations\n'
                f'- {Batch.objects.count()} Batches'
            )
        )