# Generated manually for BOL Management System

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('item_code', models.CharField(help_text='Unique item code (e.g., BX75)', max_length=20, unique=True)),
                ('item_name', models.CharField(help_text='Item name (e.g., Bauxite 75)', max_length=100)),
                ('standard_bag_weight', models.DecimalField(decimal_places=2, default=1.0, help_text='Standard weight per bag in MT', max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['item_code'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('size_label', models.CharField(help_text='Size label (e.g., -16, 3x6, 6x16)', max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['size_label'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('supplier_name', models.CharField(max_length=100, unique=True)),
                ('bol_prefix', models.CharField(help_text='BOL prefix for this supplier (e.g., YAS)', max_length=10, unique=True)),
                ('next_bol_no', models.PositiveIntegerField(default=1, help_text='Next BOL number to use')),
                ('is_active', models.BooleanField(default=True)),
                ('contact_name', models.CharField(blank=True, max_length=100)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['supplier_name'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=100, unique=True)),
                ('customer_code', models.CharField(blank=True, max_length=20)),
                ('customer_address', models.CharField(blank=True, max_length=200)),
                ('customer_city', models.CharField(blank=True, max_length=50)),
                ('customer_state', models.CharField(blank=True, max_length=2)),
                ('customer_zip', models.CharField(blank=True, max_length=10)),
                ('contact_name', models.CharField(blank=True, max_length=100)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['customer_name'],
            },
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('carrier_name', models.CharField(max_length=100, unique=True)),
                ('carrier_code', models.CharField(max_length=20, unique=True)),
                ('contact_name', models.CharField(blank=True, max_length=100)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['carrier_code'],
            },
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('truck_number', models.CharField(max_length=20)),
                ('trailer_number', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trucks', to='inventory.carrier')),
            ],
            options={
                'ordering': ['carrier__carrier_code', 'truck_number'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location_name', models.CharField(max_length=100)),
                ('location_address', models.CharField(blank=True, max_length=200)),
                ('location_city', models.CharField(blank=True, max_length=50)),
                ('location_state', models.CharField(blank=True, max_length=2)),
                ('location_zip', models.CharField(blank=True, max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='inventory.customer')),
            ],
            options={
                'ordering': ['customer__customer_name', 'location_name'],
            },
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('barcode', models.CharField(max_length=50, unique=True)),
                ('lot_number', models.CharField(blank=True, help_text='Lot number from supplier', max_length=20)),
                ('barge', models.CharField(blank=True, help_text='Barge identifier', max_length=50)),
                ('starting_quantity', models.PositiveIntegerField(help_text='Number of bags in this batch', validators=[django.core.validators.MinValueValidator(1)])),
                ('current_quantity', models.PositiveIntegerField(help_text='Current remaining bags', validators=[django.core.validators.MinValueValidator(0)])),
                ('receipt_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('DEPLETED', 'Depleted'), ('ON_HOLD', 'On Hold'), ('SHIPPED', 'Shipped')], default='ACTIVE', max_length=10)),
                ('notes', models.TextField(blank=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='inventory.item')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='inventory.size')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='inventory.supplier')),
            ],
            options={
                'verbose_name_plural': 'Batches',
                'ordering': ['-receipt_date', 'barcode'],
            },
        ),
        migrations.CreateModel(
            name='BOL',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bol_number', models.CharField(max_length=50, unique=True)),
                ('ship_date', models.DateField(default=django.utils.timezone.now)),
                ('total_bags', models.PositiveIntegerField(default=0)),
                ('total_weight_mt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('notes', models.TextField(blank=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bols', to='inventory.customer')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bols', to='inventory.location')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bols', to='inventory.supplier')),
                ('truck', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bols', to='inventory.truck')),
            ],
            options={
                'verbose_name': 'BOL',
                'verbose_name_plural': 'BOLs',
                'ordering': ['-ship_date', 'bol_number'],
            },
        ),
        migrations.CreateModel(
            name='BOLItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity_shipped', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bol_items', to='inventory.batch')),
                ('bol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.bol')),
            ],
            options={
                'ordering': ['bol', 'batch__barcode'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='truck',
            unique_together={('carrier', 'truck_number')},
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('customer', 'location_name')},
        ),
    ]