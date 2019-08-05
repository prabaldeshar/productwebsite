from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Comment
from .sentiment import makepredictions

# Create your views here.
def home(request):
    products = Products.objects
    text = "This phone is  good"
    # sentiment = makepredictions(text)
    # print(sentiment)
    return render(request,'product/home.html',{'products':products})
    # return render(request,'product/home.html',{'products':products,'text':text})



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

def post(request, product_id):
    if request.method == 'POST':
        current_user = request.user
        product = Products.objects.filter(pk=product_id).first()
        if request.POST['comment']:
            text = request.POST['comment']
            polarity = makepredictions(text)
            comment = Comment(comment= text, user=current_user,product = product, polarity=polarity)
            comment.save()
            calcRating()

            return render(request, 'product/predict.html')

def calcRating():
    products = Products.objects.all()
    total_rating=0
    pos_rating=0
    for product in products:
        comments = Comment.objects.select_related().filter(pk=product.id)
        for comment in comments:
            total_rating+=1
            if comment.polarity==1:
                pos_rating+=1
        percentage=(pos_rating/total_rating)*100
        product.rating = percentage
        product.save()
