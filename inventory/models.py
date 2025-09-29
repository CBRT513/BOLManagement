import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.urls import reverse


class TimeStampedModel(models.Model):
    """Abstract base model with created and updated timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Item(TimeStampedModel):
    """Model for items/products"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_code = models.CharField(max_length=20, unique=True, help_text="Unique item code (e.g., BX75)")
    item_name = models.CharField(max_length=100, help_text="Item name (e.g., Bauxite 75)")
    standard_bag_weight = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=1.00,
        validators=[MinValueValidator(0.01)],
        help_text="Standard weight per bag in MT"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['item_code']

    def __str__(self):
        return f"{self.item_code} - {self.item_name}"

    def get_absolute_url(self):
        return reverse('inventory:item_detail', kwargs={'pk': self.pk})


class Size(TimeStampedModel):
    """Model for size specifications"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size_label = models.CharField(max_length=20, unique=True, help_text="Size label (e.g., -16, 3x6, 6x16)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['size_label']

    def __str__(self):
        return self.size_label


class Supplier(TimeStampedModel):
    """Model for suppliers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier_name = models.CharField(max_length=100, unique=True)
    bol_prefix = models.CharField(
        max_length=10, 
        unique=True, 
        help_text="BOL prefix for this supplier (e.g., YAS)"
    )
    next_bol_no = models.PositiveIntegerField(
        default=1, 
        help_text="Next BOL number to use"
    )
    is_active = models.BooleanField(default=True)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['supplier_name']

    def __str__(self):
        return f"{self.bol_prefix} - {self.supplier_name}"

    def get_next_bol_number(self):
        """Get and increment the next BOL number"""
        current = self.next_bol_no
        self.next_bol_no += 1
        self.save()
        return current


class Customer(TimeStampedModel):
    """Model for customers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=100, unique=True)
    customer_code = models.CharField(max_length=20, blank=True)
    customer_address = models.CharField(max_length=200, blank=True)
    customer_city = models.CharField(max_length=50, blank=True)
    customer_state = models.CharField(max_length=2, blank=True)
    customer_zip = models.CharField(max_length=10, blank=True)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['customer_name']

    def __str__(self):
        return self.customer_name


class Carrier(TimeStampedModel):
    """Model for carriers/trucking companies"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carrier_name = models.CharField(max_length=100, unique=True)
    carrier_code = models.CharField(max_length=20, unique=True)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['carrier_code']

    def __str__(self):
        return f"{self.carrier_code} - {self.carrier_name}"


class Truck(TimeStampedModel):
    """Model for trucks"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='trucks')
    truck_number = models.CharField(max_length=20)
    trailer_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['carrier__carrier_code', 'truck_number']
        unique_together = ['carrier', 'truck_number']

    def __str__(self):
        trailer_info = f" - Trailer {self.trailer_number}" if self.trailer_number else ""
        return f"{self.carrier.carrier_code} Truck {self.truck_number}{trailer_info}"


class Location(TimeStampedModel):
    """Model for customer locations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='locations')
    location_name = models.CharField(max_length=100)
    location_address = models.CharField(max_length=200, blank=True)
    location_city = models.CharField(max_length=50, blank=True)
    location_state = models.CharField(max_length=2, blank=True)
    location_zip = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['customer__customer_name', 'location_name']
        unique_together = ['customer', 'location_name']

    def __str__(self):
        return f"{self.customer.customer_name} - {self.location_name}"


class Batch(TimeStampedModel):
    """Model for inventory batches"""
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('DEPLETED', 'Depleted'),
        ('ON_HOLD', 'On Hold'),
        ('SHIPPED', 'Shipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barcode = models.CharField(max_length=50, unique=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='batches')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='batches')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='batches')
    lot_number = models.CharField(max_length=20, blank=True, help_text="Lot number from supplier")
    barge = models.CharField(max_length=50, blank=True, help_text="Barge identifier")
    starting_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of bags in this batch"
    )
    current_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Current remaining bags"
    )
    receipt_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-receipt_date', 'barcode']
        verbose_name_plural = 'Batches'

    def __str__(self):
        return f"{self.barcode} - {self.item.item_code} {self.size.size_label}"

    def save(self, *args, **kwargs):
        # Auto-generate barcode if not provided
        if not self.barcode:
            lot_part = self.lot_number or ''
            barge_part = self.barge or ''
            supplier_part = self.supplier.bol_prefix if self.supplier else ''
            item_part = self.item.item_code if self.item else ''
            size_part = self.size.size_label if self.size else ''
            self.barcode = f"{barge_part}{lot_part}{supplier_part}{item_part}{size_part}"
        
        # Set current_quantity on first save
        if not self.pk and not hasattr(self, '_current_quantity_set'):
            self.current_quantity = self.starting_quantity
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory:batch_detail', kwargs={'pk': self.pk})

    @property
    def total_weight_mt(self):
        """Calculate total weight in metric tons"""
        return float(self.current_quantity) * float(self.item.standard_bag_weight)

    @property
    def is_depleted(self):
        """Check if batch is depleted"""
        return self.current_quantity == 0

    def update_quantity(self, new_quantity):
        """Update current quantity and status"""
        self.current_quantity = max(0, new_quantity)
        if self.current_quantity == 0:
            self.status = 'DEPLETED'
        self.save()


class BOL(TimeStampedModel):
    """Model for Bills of Lading"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bol_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='bols')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bols')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='bols', null=True, blank=True)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='bols', null=True, blank=True)
    ship_date = models.DateField(default=timezone.now)
    total_bags = models.PositiveIntegerField(default=0)
    total_weight_mt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-ship_date', 'bol_number']
        verbose_name = 'BOL'
        verbose_name_plural = 'BOLs'

    def __str__(self):
        return f"BOL {self.bol_number} - {self.customer.customer_name}"


class BOLItem(TimeStampedModel):
    """Model for individual items on a BOL"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bol = models.ForeignKey(BOL, on_delete=models.CASCADE, related_name='items')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='bol_items')
    quantity_shipped = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['bol', 'batch__barcode']

    def __str__(self):
        return f"{self.bol.bol_number} - {self.batch.barcode} ({self.quantity_shipped} bags)"

    @property
    def weight_mt(self):
        """Calculate weight in metric tons"""
        return float(self.quantity_shipped) * float(self.batch.item.standard_bag_weight)