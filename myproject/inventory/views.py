from django.shortcuts import render
from .models import Supplier, Material, Delivery

def home(request):
    suppliers = Supplier.objects.all()
    materials = Material.objects.all()
    deliveries = Delivery.objects.all()
    
    context = {
        'suppliers': suppliers,
        'materials': materials,
        'deliveries': deliveries
    }
    
    return render(request, 'inventory/home.html', context)

