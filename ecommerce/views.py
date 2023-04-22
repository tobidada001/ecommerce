from django.shortcuts import render, get_object_or_404, redirect
from ecommerce.models import Product, Brand, ProductCategory, ProductSize, CustomerReview
from ecommerce.models import Cart, CartItems, ProductVariation, Color, Order
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.db.models import Q
from pprint import pprint
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib import messages, auth
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
# Create your views here.

def index(request):
    products = Product.objects.all()
    for product in products:
        sizes = ProductSize.objects.filter(id__in = product.product_variation.all().values_list('size', flat = True).distinct())
        colors = Color.objects.filter(id__in = product.product_variation.all().values_list('color', flat = True).distinct())
        product.product_variation.size_list = sizes
        product.product_variation.color_list = colors
        

    context = { 'products': products }
    return render(request, 'ecommerce/index.html', context)


def shop(request):
    
    brands = Brand.objects.all()
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    
    for product in products:
        sizes = ProductSize.objects.filter(id__in = product.product_variation.all().values_list('size', flat = True).distinct())
        colors = Color.objects.filter(id__in = product.product_variation.all().values_list('color', flat = True).distinct())
        product.product_variation.size_list = sizes
        product.product_variation.color_list = colors

    pages = Paginator(products, 12)


    page_number = request.GET.get('page', 1)
    page = pages.get_page(page_number)
    
    page.adjusted_elided_pages = pages.get_elided_page_range(page_number)
    
    context = {'brands': brands, 'categories': categories, 'sizes': sizes, 'products': products, 'page': page}
    return render(request, 'ecommerce/shop.html', context)

def product_details(request, pk):
    product = get_object_or_404(Product, id = pk)
    category = get_object_or_404(ProductCategory, category_name = product.category)
    brand = get_object_or_404(Brand, name = product.brand)
    
    related_products = category.products.all()
    related_brands = brand.brand_products.all()

    sizes = ProductSize.objects.filter(id__in = product.product_variation.all().values_list('size', flat = True).distinct())
    colors = Color.objects.filter(id__in = product.product_variation.all().values_list('color', flat = True).distinct())
    product.product_variation.size_list = sizes
    product.product_variation.color_list = colors

    return render(request, 'ecommerce/shop-details.html', {'product': product, 'related_brands': related_brands, 'related_products': related_products})


def cart(request):
    context = {}
    if request.user.is_authenticated:
        items = Cart.objects.filter(owner = request.user).last()
        
        if items:
            context = {
                'items_in_cart': items.cart_items.all(), 'total_amount_to_pay': items.total_amount_to_pay}
        else:
            context = {}
           
    return render(request, 'ecommerce/shopping-cart.html', context)



def add_to_cart(request):

    response = 0
    if request.method == 'GET':
        
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id = product_id) 
        color = request.GET.get('color')
        size = request.GET.get('size')
        num_of_products = request.GET.get('num_of_products')
        path = request.GET.get('path')
        
        if request.user.is_authenticated:
            
            variation = ProductVariation.objects.filter(product_id = product.id,  size_id = size).last()
            cart, created_cart = Cart.objects.get_or_create(owner=request.user)
            item, created_item = CartItems.objects.get_or_create(product_id = product.id, items = cart, variation = variation)
            
            item.save()
            if num_of_products:
                item.quantity += int(num_of_products)
                
            else:
                item.quantity += 1
        
            item.save()

            response =  cart.total_in_cart

            if path:
                return redirect(request.GET['path'])

            return HttpResponse(response)

    return HttpResponse(response)


def update_cart(request):
    response = 0
    if request.method == 'GET':
        new_quantity = request.GET['new_quantity']
        p_id = request.GET['product_id']
        
        cart, created_cart = Cart.objects.get_or_create(owner=request.user)
        try:
            item, created_item = CartItems.objects.get_or_create(id = p_id, items = cart)
        except:
            print('Cannot find it.')
            item, created_item = CartItems.objects.get_or_create(product_id = p_id, items = cart)

        item.quantity = int(new_quantity)
        item.save()

        response = {
            'cart_items_total': cart.total_in_cart,
            'item_subtotal': float(item.total_amount),
            'total_payment': float(cart.total_amount_to_pay)
        }

    return JsonResponse(response)

def remove_from_cart(request):
    if request.method == 'GET':
        cart_list = []
        
        cartitemid = request.GET['product_id']
        cart = Cart.objects.filter(owner = request.user).last()

        item = CartItems.objects.filter(items = cart, id = cartitemid)
        if item.exists():
            item.delete()
        else:
            print('Item does not exist')

        items = cart.cart_items.select_related('product').all()

        item  = items.filter().last()
        if item:
            context = { 'subtotal': item.total_amount,
            'total_product_quantity': cart.total_in_cart, 'total_payment': cart.total_amount_to_pay }
        else:
            context = { 'subtotal': 0,
            'total_product_quantity': 0, 'total_payment': 0 }

        rendered = {'table_to_render': render_to_string('ecommerce/returned_row.html', context = {'data': items})}

    return JsonResponse({'rendered': rendered, 'data': context}, safe=False)


def load_colors(request):
    context = []
    size_id = request.GET['sizeid']
    product_id = request.GET['p_id']
    product = Product.objects.filter(id = product_id).last()
    data = product.product_variation.filter(size_id = size_id)

    c = {'data': data, 'product': product}
    rendered = {'table_to_render': render_to_string('ecommerce/colors_list.html', context = c)}
   
    return JsonResponse(rendered, safe= False)


@login_required(login_url = '/shop/')
def checkout(request):
    cart = Cart.objects.filter(owner = request.user).last()
    
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        country = request.POST['country']
        address = request.POST['address']
        city = request.POST['city']
        zip = request.POST['zip']
        phone = request.POST['phone']
        email = request.POST['email']
        method = request.POST['paymenttype']
        
        my_order = Order(user = request.user, first_name = fname, last_name = lname, 
        email = email, address = address, city = city, zip = zip, phone = phone, country = country,
        total_amount = cart.total_amount_to_pay, payment_method = method
        )

        if Order.objects.filter(order_id = my_order.order_id).exists():
            my_order.order_id = str(uuid.uuid4())[:8]
        my_order.save()

        Cart.objects.filter(owner = request.user).delete()

    return render(request, 'ecommerce/checkout.html', {'cart': cart})


def discount(request):
    return HttpResponse('Discount added')

def orders(request):

    if request.user.is_authenticated: 
        orders = request.user.order_set.all()
    else:
        orders = ''
    return render(request, 'ecommerce/orders.html', {'orders': orders})


def auth_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        
        if User.objects.filter(Q(username=username) | Q(password=password)).exists():
            the_user = auth.authenticate(username = username, password=password)
            
            if the_user.is_authenticated:
                login(request, the_user)
                return redirect('/')
            else:
                
                return redirect(request.path)
        else:
            return redirect(request.path)

    return render(request, 'ecommerce/signin.html')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')    
    
    if request.method == 'POST':
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        c_pass = request.POST['c_password']

        if not password == c_pass:
            messages.error(request, 'Please make sure both password fields have the same data.')
        else:
            if User.objects.filter(username = username).exists() or User.objects.filter(email = email).exists():
                messages.error(request, 'Username or email already exists. Please check to make sure you haven\'t used any of them before.')
            else:
                User.objects.create_user(username = username, email = email, password = password)
                print('User created successfully.')

                return redirect('/auth-user/')

    return render(request, 'ecommerce/signup.html')


def logoutuser(request):

    logout(request)
    return redirect('/')


def justtest(request):

    if request.method == 'POST':
        print('THIS IS THE POST DATA: ', request.POST)
    return render(request, 'AjaxPostDemo.html')