from django.shortcuts import render, redirect, get_object_or_404
from .models import Products

# Create your views here.
def home(request):
    products = Products.objects
    return render(request,'product/home.html',{'products':products})\

def add(request):
    if request.method=='POST':
        if request.POST['title'] and request.FILES['image'] and request.POST['manufacturer'] and request.POST['description'] and request.POST['price']:
            product = Products()

            product.title = request.POST['title']
            product.image = request.FILES['image']
            product.manufacturer = request.POST['manufacturer']
            product.description = request.POST['description']
            product.price = request.POST['price']

            product.save()

            return redirect('home')

        else:
            return render(request,'product/add.html',{'error':'All Fields required'})

    else:
        return render(request,'product/add.html')

def detail(request, product_id):
    product = get_object_or_404(Products, pk= product_id)
    return render(request, 'product/detail.html', {'product':product})
