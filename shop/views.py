from django.shortcuts import render, redirect
from .models import Product, Order

# List all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# Add product to the cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    return redirect('product_list')

# View cart
def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'shop/cart.html', {'cart': cart, 'total': total})

# Checkout
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            Order.objects.create(product=product, quantity=item['quantity'])
        
        request.session['cart'] = {}  # Empty the cart after checkout
        return redirect('product_list')

    return render(request, 'shop/checkout.html')
