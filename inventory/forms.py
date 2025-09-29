from django import forms
from .models import (
    Item, Size, Supplier, Customer, Carrier, Truck,
    Location, Batch, BOL, BOLItem
)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_code', 'item_name', 'standard_bag_weight', 'is_active']
        widgets = {
            'item_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., BX75'
            }),
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bauxite 75'
            }),
            'standard_bag_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '1.00'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size_label', 'is_active']
        widgets = {
            'size_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., -16, 3x6, 6x16'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'supplier_name', 'bol_prefix', 'next_bol_no', 'contact_name',
            'contact_phone', 'contact_email', 'notes', 'is_active'
        ]
        widgets = {
            'supplier_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., YAS Industries'
            }),
            'bol_prefix': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., YAS'
            }),
            'next_bol_no': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '555-1234'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@supplier.com'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_name', 'customer_code', 'customer_address',
            'customer_city', 'customer_state', 'customer_zip',
            'contact_name', 'contact_phone', 'contact_email',
            'notes', 'is_active'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer name'
            }),
            'customer_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer code'
            }),
            'customer_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address'
            }),
            'customer_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'customer_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ST',
                'maxlength': '2'
            }),
            'customer_zip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345'
            }),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '555-1234'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@customer.com'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = [
            'carrier_name', 'carrier_code', 'contact_name',
            'contact_phone', 'contact_email', 'notes', 'is_active'
        ]
        widgets = {
            'carrier_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., ABC Trucking'
            }),
            'carrier_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., ABC'
            }),
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '555-1234'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@carrier.com'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['carrier', 'truck_number', 'trailer_number', 'is_active']
        widgets = {
            'carrier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'truck_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 123'
            }),
            'trailer_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., T456'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrier'].queryset = Carrier.objects.filter(is_active=True)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'customer', 'location_name', 'location_address',
            'location_city', 'location_state', 'location_zip', 'is_active'
        ]
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location name'
            }),
            'location_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address'
            }),
            'location_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'location_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ST',
                'maxlength': '2'
            }),
            'location_zip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True)


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            'barcode', 'item', 'size', 'supplier', 'lot_number', 'barge',
            'starting_quantity', 'receipt_date', 'status', 'notes'
        ]
        widgets = {
            'barcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-generated if left blank'
            }),
            'item': forms.Select(attrs={
                'class': 'form-select'
            }),
            'size': forms.Select(attrs={
                'class': 'form-select'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lot_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lot number'
            }),
            'barge': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Barge identifier'
            }),
            'starting_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of bags'
            }),
            'receipt_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(is_active=True)
        self.fields['size'].queryset = Size.objects.filter(is_active=True)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True)


class BOLForm(forms.ModelForm):
    class Meta:
        model = BOL
        fields = [
            'bol_number', 'supplier', 'customer', 'location', 'truck',
            'ship_date', 'notes'
        ]
        widgets = {
            'bol_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'BOL Number'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'customer': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.Select(attrs={
                'class': 'form-select'
            }),
            'truck': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ship_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True)
        self.fields['location'].queryset = Location.objects.filter(is_active=True)
        self.fields['truck'].queryset = Truck.objects.filter(is_active=True)


class BOLItemForm(forms.ModelForm):
    class Meta:
        model = BOLItem
        fields = ['batch', 'quantity_shipped']
        widgets = {
            'batch': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantity_shipped': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Bags to ship'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.filter(
            status='ACTIVE', 
            current_quantity__gt=0
        ).select_related('item', 'size')