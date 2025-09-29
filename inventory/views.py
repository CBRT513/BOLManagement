import json
import logging
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, 
    UpdateView, DeleteView, View
)
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Sum, Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

from .models import (
    Item, Size, Supplier, Customer, Carrier, Truck,
    Location, Batch, BOL, BOLItem
)
from .forms import (
    ItemForm, SizeForm, SupplierForm, CustomerForm,
    CarrierForm, TruckForm, LocationForm, BatchForm
)

logger = logging.getLogger(__name__)


class MainMenuView(TemplateView):
    """Main menu view that matches your existing SPA menu"""
    template_name = 'inventory/main_menu.html'


# ==== ITEM VIEWS ====
class ItemListView(ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'
    queryset = Item.objects.filter(is_active=True)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'inventory/item_detail.html'


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('inventory:item_list')

    def form_valid(self, form):
        messages.success(self.request, 'Item added successfully!')
        return super().form_valid(form)


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('inventory:item_list')

    def form_valid(self, form):
        messages.success(self.request, 'Item updated successfully!')
        return super().form_valid(form)


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:item_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Item deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== SIZE VIEWS ====
class SizeListView(ListView):
    model = Size
    template_name = 'inventory/size_list.html'
    context_object_name = 'sizes'
    queryset = Size.objects.filter(is_active=True)


class SizeCreateView(CreateView):
    model = Size
    form_class = SizeForm
    template_name = 'inventory/size_form.html'
    success_url = reverse_lazy('inventory:size_list')

    def form_valid(self, form):
        messages.success(self.request, 'Size added successfully!')
        return super().form_valid(form)


class SizeDeleteView(DeleteView):
    model = Size
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:size_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Size deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== SUPPLIER VIEWS ====
class SupplierListView(ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'
    queryset = Supplier.objects.filter(is_active=True)


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'inventory/supplier_detail.html'


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('inventory:supplier_list')

    def form_valid(self, form):
        messages.success(self.request, 'Supplier added successfully!')
        return super().form_valid(form)


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('inventory:supplier_list')

    def form_valid(self, form):
        messages.success(self.request, 'Supplier updated successfully!')
        return super().form_valid(form)


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:supplier_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Supplier deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== CUSTOMER VIEWS ====
class CustomerListView(ListView):
    model = Customer
    template_name = 'inventory/customer_list.html'
    context_object_name = 'customers'
    queryset = Customer.objects.filter(is_active=True)


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'inventory/customer_detail.html'


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'inventory/customer_form.html'
    success_url = reverse_lazy('inventory:customer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Customer added successfully!')
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'inventory/customer_form.html'
    success_url = reverse_lazy('inventory:customer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully!')
        return super().form_valid(form)


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:customer_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Customer deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== CARRIER VIEWS ====
class CarrierListView(ListView):
    model = Carrier
    template_name = 'inventory/carrier_list.html'
    context_object_name = 'carriers'
    queryset = Carrier.objects.filter(is_active=True)


class CarrierDetailView(DetailView):
    model = Carrier
    template_name = 'inventory/carrier_detail.html'


class CarrierCreateView(CreateView):
    model = Carrier
    form_class = CarrierForm
    template_name = 'inventory/carrier_form.html'
    success_url = reverse_lazy('inventory:carrier_list')

    def form_valid(self, form):
        messages.success(self.request, 'Carrier added successfully!')
        return super().form_valid(form)


class CarrierUpdateView(UpdateView):
    model = Carrier
    form_class = CarrierForm
    template_name = 'inventory/carrier_form.html'
    success_url = reverse_lazy('inventory:carrier_list')

    def form_valid(self, form):
        messages.success(self.request, 'Carrier updated successfully!')
        return super().form_valid(form)


class CarrierDeleteView(DeleteView):
    model = Carrier
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:carrier_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Carrier deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== TRUCK VIEWS ====
class TruckListView(ListView):
    model = Truck
    template_name = 'inventory/truck_list.html'
    context_object_name = 'trucks'
    queryset = Truck.objects.filter(is_active=True).select_related('carrier')


class TruckDetailView(DetailView):
    model = Truck
    template_name = 'inventory/truck_detail.html'


class TruckCreateView(CreateView):
    model = Truck
    form_class = TruckForm
    template_name = 'inventory/truck_form.html'
    success_url = reverse_lazy('inventory:truck_list')

    def form_valid(self, form):
        messages.success(self.request, 'Truck added successfully!')
        return super().form_valid(form)


class TruckUpdateView(UpdateView):
    model = Truck
    form_class = TruckForm
    template_name = 'inventory/truck_form.html'
    success_url = reverse_lazy('inventory:truck_list')

    def form_valid(self, form):
        messages.success(self.request, 'Truck updated successfully!')
        return super().form_valid(form)


class TruckDeleteView(DeleteView):
    model = Truck
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:truck_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Truck deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== LOCATION VIEWS ====
class LocationListView(ListView):
    model = Location
    template_name = 'inventory/location_list.html'
    context_object_name = 'locations'
    queryset = Location.objects.filter(is_active=True).select_related('customer')


class LocationDetailView(DetailView):
    model = Location
    template_name = 'inventory/location_detail.html'


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'inventory/location_form.html'
    success_url = reverse_lazy('inventory:location_list')

    def form_valid(self, form):
        messages.success(self.request, 'Location added successfully!')
        return super().form_valid(form)


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'inventory/location_form.html'
    success_url = reverse_lazy('inventory:location_list')

    def form_valid(self, form):
        messages.success(self.request, 'Location updated successfully!')
        return super().form_valid(form)


class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:location_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Location deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== BATCH VIEWS ====
class BatchListView(ListView):
    model = Batch
    template_name = 'inventory/batch_list.html'
    context_object_name = 'batches'
    queryset = Batch.objects.select_related('item', 'size', 'supplier')
    paginate_by = 50


class BatchDetailView(DetailView):
    model = Batch
    template_name = 'inventory/batch_detail.html'


class BatchCreateView(CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'inventory/batch_form.html'
    success_url = reverse_lazy('inventory:batch_list')

    def form_valid(self, form):
        messages.success(self.request, 'Batch added successfully!')
        return super().form_valid(form)


class BatchUpdateView(UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'inventory/batch_form.html'
    success_url = reverse_lazy('inventory:batch_list')

    def form_valid(self, form):
        messages.success(self.request, 'Batch updated successfully!')
        return super().form_valid(form)


class BatchDeleteView(DeleteView):
    model = Batch
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:batch_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Batch deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==== API VIEWS (for AJAX calls matching your existing system) ====

class BaseAPIView(View):
    """Base class for API views"""
    
    def get_success_response(self, data=None, message="Success"):
        return JsonResponse({
            'success': True,
            'message': message,
            'data': data
        }, encoder=DjangoJSONEncoder)
    
    def get_error_response(self, message="Error occurred", status=400):
        return JsonResponse({
            'success': False,
            'message': message
        }, status=status)


@method_decorator(csrf_exempt, name='dispatch')
class ItemAPIView(BaseAPIView):
    """API View for Items - matches your Google Scripts functions"""
    
    def get(self, request):
        """Get all items - matches getItems()"""
        try:
            items = []
            for item in Item.objects.filter(is_active=True):
                items.append({
                    'itemId': str(item.id),
                    'itemCode': item.item_code,
                    'itemName': item.item_name,
                    'standardBagWeight': float(item.standard_bag_weight)
                })
            return JsonResponse(items, safe=False)
        except Exception as e:
            logger.error(f"Error getting items: {e}")
            return self.get_error_response("Error loading items")
    
    def post(self, request):
        """Add new item - matches addItem()"""
        try:
            data = json.loads(request.body)
            item = Item.objects.create(
                item_code=data['itemCode'],
                item_name=data['itemName'],
                standard_bag_weight=data['standardBagWeight']
            )
            return self.get_success_response({
                'id': str(item.id)
            }, "Item added successfully")
        except Exception as e:
            logger.error(f"Error adding item: {e}")
            return self.get_error_response("Error adding item")
    
    def put(self, request):
        """Update item - matches updateItem()"""
        try:
            data = json.loads(request.body)
            item = Item.objects.get(id=data['itemId'])
            item.item_code = data['itemCode']
            item.item_name = data['itemName']
            item.standard_bag_weight = data['standardBagWeight']
            item.save()
            return self.get_success_response(message="Item updated successfully")
        except Item.DoesNotExist:
            return self.get_error_response("Item not found", 404)
        except Exception as e:
            logger.error(f"Error updating item: {e}")
            return self.get_error_response("Error updating item")
    
    def delete(self, request):
        """Delete item - matches deleteItem()"""
        try:
            data = json.loads(request.body)
            item = Item.objects.get(id=data['itemId'])
            item.delete()
            return self.get_success_response(message="Item deleted successfully")
        except Item.DoesNotExist:
            return self.get_error_response("Item not found", 404)
        except Exception as e:
            logger.error(f"Error deleting item: {e}")
            return self.get_error_response("Error deleting item")


@method_decorator(csrf_exempt, name='dispatch')
class SizeAPIView(BaseAPIView):
    """API View for Sizes - matches your Google Scripts functions"""
    
    def get(self, request):
        """Get all sizes - matches getSizes()"""
        try:
            sizes = []
            for size in Size.objects.filter(is_active=True):
                sizes.append({
                    'sizeId': str(size.id),
                    'sizeLabel': size.size_label
                })
            return JsonResponse(sizes, safe=False)
        except Exception as e:
            logger.error(f"Error getting sizes: {e}")
            return self.get_error_response("Error loading sizes")
    
    def post(self, request):
        """Add new size - matches addSize()"""
        try:
            data = json.loads(request.body)
            size = Size.objects.create(size_label=data['sizeLabel'])
            return self.get_success_response({
                'id': str(size.id)
            }, "Size added successfully")
        except Exception as e:
            logger.error(f"Error adding size: {e}")
            return self.get_error_response("Error adding size")
    
    def delete(self, request):
        """Delete size - matches deleteSize()"""
        try:
            data = json.loads(request.body)
            size = Size.objects.get(id=data['sizeId'])
            size.delete()
            return self.get_success_response(message="Size deleted successfully")
        except Size.DoesNotExist:
            return self.get_error_response("Size not found", 404)
        except Exception as e:
            logger.error(f"Error deleting size: {e}")
            return self.get_error_response("Error deleting size")


# Similar API views for other models...
@method_decorator(csrf_exempt, name='dispatch')
class SupplierAPIView(BaseAPIView):
    def get(self, request):
        suppliers = []
        for supplier in Supplier.objects.filter(is_active=True):
            suppliers.append({
                'supplierId': str(supplier.id),
                'supplierName': supplier.supplier_name,
                'bolPrefix': supplier.bol_prefix,
                'nextBolNo': supplier.next_bol_no,
                'active': supplier.is_active
            })
        return JsonResponse(suppliers, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CustomerAPIView(BaseAPIView):
    def get(self, request):
        customers = []
        for customer in Customer.objects.filter(is_active=True):
            customers.append({
                'customerId': str(customer.id),
                'customerName': customer.customer_name,
                'customerCode': customer.customer_code
            })
        return JsonResponse(customers, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CarrierAPIView(BaseAPIView):
    def get(self, request):
        carriers = []
        for carrier in Carrier.objects.filter(is_active=True):
            carriers.append({
                'carrierId': str(carrier.id),
                'carrierName': carrier.carrier_name,
                'carrierCode': carrier.carrier_code,
                'contactName': carrier.contact_name or '',
                'contactPhone': carrier.contact_phone or ''
            })
        return JsonResponse(carriers, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TruckAPIView(BaseAPIView):
    def get(self, request):
        trucks = []
        for truck in Truck.objects.filter(is_active=True).select_related('carrier'):
            trucks.append({
                'truckId': str(truck.id),
                'carrierId': str(truck.carrier.id),
                'truckNo': truck.truck_number,
                'trailerNo': truck.trailer_number or '',
                'carrierName': truck.carrier.carrier_name,
                'carrierCode': truck.carrier.carrier_code
            })
        return JsonResponse(trucks, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class LocationAPIView(BaseAPIView):
    def get(self, request):
        locations = []
        for location in Location.objects.filter(is_active=True).select_related('customer'):
            locations.append({
                'locationId': str(location.id),
                'customerId': str(location.customer.id),
                'locationName': location.location_name,
                'locationAddress': location.location_address or '',
                'locationCity': location.location_city or '',
                'locationState': location.location_state or '',
                'locationZip': location.location_zip or ''
            })
        return JsonResponse(locations, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class BatchAPIView(BaseAPIView):
    def get(self, request):
        batches = []
        for batch in Batch.objects.select_related('item', 'size', 'supplier'):
            batches.append({
                'batchId': str(batch.id),
                'barcode': batch.barcode,
                'itemId': str(batch.item.id),
                'sizeId': str(batch.size.id),
                'itemCode': batch.item.item_code,
                'sizeLabel': batch.size.size_label,
                'supplier': batch.supplier.supplier_name,
                'lotNo': batch.lot_number or '',
                'barge': batch.barge or '',
                'startingQuantity': batch.starting_quantity,
                'receiptDate': batch.receipt_date.strftime('%Y-%m-%d'),
                'status': batch.get_status_display()
            })
        return JsonResponse(batches, safe=False)


class ReportsView(TemplateView):
    """Reports and BOL generation view"""
    template_name = 'inventory/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add summary statistics
        context['total_batches'] = Batch.objects.count()
        context['active_batches'] = Batch.objects.filter(status='ACTIVE').count()
        context['total_items'] = Item.objects.filter(is_active=True).count()
        context['total_suppliers'] = Supplier.objects.filter(is_active=True).count()
        
        # Recent activity
        context['recent_batches'] = Batch.objects.select_related(
            'item', 'size', 'supplier'
        ).order_by('-created_at')[:10]
        
        return context