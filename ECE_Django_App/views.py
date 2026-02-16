from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Product
from django.views.decorators.cache import never_cache
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializer import ProductSerializers


# Create your views here.

# for HTML Pages
def homepage(request):
    return render(request, 'index.html')

def aboutuspage(request):
    return render(request, 'aboutus.html')

def loginform(request):
    return render(request, 'login.html')

def home2(request):
    return render(request, 'home.html')

def add_product_page(request):
    return render(request, 'add_product.html')

def product_search_page(request):
    return render(request, 'product_search.html')

def modify_product_page(request):
    return render(request, 'modify_product.html')

def delete_product_page(request):
    return render(request, 'delete_product.html')
    

# Logical Functions

# Data Insert
def user_register(request):
    if request.method == "POST":
        Student.objects.create(
            name = request.POST.get('fname'),
            email = request.POST.get('email'),
            password = request.POST.get('password'),
            college = request.POST.get('college')
        )
        return render(request, 'login.html')
    return render(request, 'index.html')


# User Login
def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(email = email, password = password)
            request.session['student_id'] = student.id
            request.session['email'] = student.email
            # return render(request, 'home.html')
            return redirect('/afterlogin')
        except Student.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html')


# User Logout
def logout(request):
    request.session.flush()
    return render(request, 'login.html')

@never_cache
# Session Protected Home Page
def afterlogin_home(request):
    if 'student_id' not in request.session:
        return render(request, 'login.html')
    
    student = Student.objects.get(id = request.session['student_id'])
    return render(request, 'home.html', {'student': student})  # {'name': student.name}


# Add Product
def add_product(request):
    if request.method == "POST":
        Product.objects.create(
            pname = request.POST.get('pname'),
            bname = request.POST.get('bname'),
            price = request.POST.get('price')
        )
        return render(request, 'add_product.html')
    return render(request, 'index.html')


# Search Product
def search_product(request):
    query = request.GET.get('q')
    products = []

    if query:
        products = Product.objects.filter(
            Q(pname__icontains=query) | Q(bname__icontains=query)
        )

    return render(request, 'product_search.html', {'products': products, 'query': query})


# Product Update
def product_details_update(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == "POST":
        product.pname = request.POST.get('pname')
        product.price = request.POST.get('price')

        product.save()
        
        return redirect('/product_search_page')
    
    return render(request, 'modify_product.html', {'product': product})


# product delete
def product_details_delete(request, id):
    product = get_object_or_404(Product, id=id)

    product.delete()
    return redirect('/product_search_page')


# API Development for PRODUCT Model 

# Product List create using API
@api_view(['GET', 'POST'])
def add_product_api(request):

    if request.method == 'GET':
        product = Product.objects.all()  # store the data into a variable
        serializer = ProductSerializers(product, many = True)    # tranfser the data from variable to RFW variable
        return Response(serializer.data)   # show the output as RESPONSE
    
    if request.method == 'POST':
        serializer = ProductSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def all_product_details(request, id):
    try:
        product = Product.objects.get(id = id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = ProductSerializers(product, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)