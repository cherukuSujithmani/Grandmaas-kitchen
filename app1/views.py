
from django.shortcuts import render, redirect, get_object_or_404
from .forms import Regform, LoginForm,AddressForm
from django.contrib.auth import login as auth_login, authenticate, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product,Order, OrderItem,Wishlist,Address,Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import send_order_confirmation_email
from django.db.models import Q
from .models import Profile  # Make sure this import is at the top

def register(request):
    if request.method == 'POST':
        form = Regform(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the user
            Profile.objects.create(user=user)  # ✅ Create profile for the user
            return redirect('app1:login')  # Redirect to login
        else:
            return render(request, 'reg.html', {'form': form})
    else:
        form = Regform()  # Initialize the form for GET requests
    return render(request, 'reg.html', {'form': form})
# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Assuming LoginForm is a custom form for login
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Use auth_login to log the user in
                return redirect('app1:home1')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})  # Add a custom error message
    else:
        form = LoginForm()  # Initialize the login form for GET requests
    return render(request, 'login.html', {'form': form})


# Home View (requires login)
# @login_required(login_url='app1:login')
# def home(request):
#     data = request.user
#     return render(request, 'home.html', {'data': data})



# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('app1:home1')

def home_view(request):
    return render(request, 'home1.html')


  # Import the Product model

def pickles(request):
    pickles = Product.objects.filter(category="Pickles")  # Get only Pickles category
    filter_type = request.GET.get("filter")  # Get filter value from URL query parameters

    if filter_type == "veg":
        pickles = pickles.filter(pickle_type="veg")  # ✅ Corrected field name
    elif filter_type == "nonveg":
        pickles = pickles.filter(pickle_type="nonveg")  # ✅ Corrected field name
    elif filter_type == "lowtohigh":
        pickles = pickles.order_by("price")  # ✅ Correct sorting

    return render(request, "pickles.html", {"products": pickles})


def sweets(request):
    sweets = Product.objects.filter(category="Sweets")  # Get only Sweets category
    filter_type = request.GET.get("filter")  # Get filter value from URL query parameters

    if filter_type == "sugar":
        sweets = sweets.filter(sweet_type="Sugar")  # Correct field name
    elif filter_type == "nosugar":
        sweets = sweets.filter(sweet_type="No-Sugar")  # Correct field name
    elif filter_type == "lowtohigh":
        sweets = sweets.order_by("price")  # Sort by price ascending

    return render(request, "sweets.html", {"products": sweets})


def snacks(request):
    snacks = Product.objects.filter(category="Snacks")  # Get only Snacks category
    return render(request, "snacks.html", {"products": snacks})





# Cart View - Displays items in the cart
def cart(request):

    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * item['quantity']
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})


# Add to Cart View


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        product = get_object_or_404(Product, id=product_id)
        cart[str(product_id)] = {'quantity': 1}

    request.session['cart'] = cart  # Save cart to session

    # Return a JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Item added to cart! 🛒'
        })
    else:
        return redirect('app1:cart')  # Handle non-AJAX requests

# Update Cart Quantity View
def update_cart(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity

        request.session['cart'] = cart
    return redirect('app1:cart')


# Remove from Cart View
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('app1:cart')

#  checkout view

# Import OrderItem

@login_required
@csrf_exempt  # ⚠️ Remove if you're using {% csrf_token %} in the form
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * item['quantity']
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found."})

    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        selected_address_str = None
        phone = None

        # Check if user added a new address
        if request.POST.get("full_name") and request.POST.get("street"):
            # Get new address details from POST
            full_name = request.POST.get("full_name")
            street = request.POST.get("street")
            city = request.POST.get("city")
            state = request.POST.get("state")
            postal_code = request.POST.get("postal_code")
            country = request.POST.get("country")
            phone = request.POST.get("phone")

            # Create new address
            new_address = Address.objects.create(
                user=request.user,
                full_name=full_name,
                street=street,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                phone=phone
            )

            selected_address_str = f"{full_name}, {street}, {city}, {state} - {postal_code}, {country}"
        else:
            # Use saved address
            address_id = request.POST.get("selected_address")
            try:
                selected_address = Address.objects.get(id=address_id, user=request.user)
                selected_address_str = f"{selected_address.full_name}, {selected_address.street}, {selected_address.city}, {selected_address.state} - {selected_address.postal_code}, {selected_address.country}"
                phone = selected_address.phone
            except Address.DoesNotExist:
                return JsonResponse({"success": False, "message": "Selected address not found."})

        payment_method = request.POST.get("payment_method")

        if not selected_address_str or not payment_method:
            return JsonResponse({"success": False, "message": "Address or payment method missing."})

        try:
            # Create the order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                address=selected_address_str,
                phone=phone if phone else request.user.profile.phone,
                payment_method=payment_method,
                status="Pending"
            )

            # Add items to the order
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price * item['quantity']
                )
            # Send confirmation email to the user
            send_order_confirmation_email(request.user, order)
            request.session["cart"] = {}
            return redirect('app1:order_confirmation', order_id=order.id)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "addresses": addresses
    })

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)  # Fetch items for the order

    return render(request, "order_confirmation.html", {
        "order": order,
        "order_items": order_items  # Pass order items to the template
    })

# successful confirmation
# def order_success(request):
#     return render(request, 'order_success.html')

@login_required
def order_history(request):
    # Get only the orders of the currently logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "order_history.html", {"orders": orders})



# wishlist views.
@login_required
def wishlist(request):
    """Display the wishlist for the logged-in user."""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"wishlist_items": wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    """Add a product to the wishlist."""
    product = get_object_or_404(Product, id=product_id)

    # Check if product is already in wishlist
    if Wishlist.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({"success": False, "message": "Product already in wishlist!"})

    Wishlist.objects.create(user=request.user, product=product)
    return JsonResponse({"success": True, "message": "Added to wishlist!"})

@login_required
def remove_from_wishlist(request, product_id):
    """Remove a product from the wishlist."""
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return JsonResponse({"success": True, "message": "Removed from wishlist!"})


# profile view
@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    address_form = AddressForm()

    context = {
        'orders': orders,
        'wishlist': wishlist,
        'addresses': addresses,
        'address_form': address_form,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user.username = username
        user.email = email

        if new_password or confirm_new_password:
            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return redirect('app1:profile')

            if new_password != confirm_new_password:
                messages.error(request, "New passwords do not match.")
                return redirect('app1:profile')

            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Keep user logged in
            # messages.success(request, "Password updated successfully.")  # ✅ Success message here

        user.save()
        messages.success(request, "Profile updated successfully.")  # ✅ Also shows profile update success

        return redirect('app1:profile')

    return render(request, 'profile.html')


# address views
@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('app1:profile')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})


@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('app1:profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'address_form.html', {'form': form, 'address': address})

@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('app1:profile')  # Make sure this name matches your profile URL name
    return redirect('app1:profile')


# search functionality for products
# views.py

def search_products(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'search_results.html', {'query': query, 'results': results})

# Search products
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# upload image 
@login_required
def update_profile_photo(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = Profile.objects.get(user=request.user)
        profile.profile_image = request.FILES['profile_image']
        profile.save()
    return redirect('app1:profile')  # redirect to profile page

# about profile
def about(request):
    return render(request, 'about.html')
def contactus(request):
    return render(request, 'contactus.html')