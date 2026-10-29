from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """View to display all available products on the home page"""
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    """View to display details of a single product"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'store/cart_detail.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_detail')


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('product_list')
    
    total = sum(item.total_price for item in cart_items)
    
    # Create the Order
    order = Order.objects.create(user=request.user, total_price=total, status='Completed')
    
    # Create OrderItems and clear cart
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity
        )
    cart_items.delete()
    
    return render(request, 'store/order_success.html', {'order': order})

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('product_list')