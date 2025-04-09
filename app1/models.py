from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.core.validators import RegexValidator
from django.conf import settings 

class Account(AbstractUser):
    phone = models.CharField(
        max_length=10, 
        validators=[RegexValidator(r'^\d{10}$', message="Enter a valid 10-digit phone number.")]
    )
    address = models.CharField(max_length=100)
    
# models for products 
# Category Choices
CATEGORY_CHOICES = [
    ('Pickles', 'Pickles'),
    ('Sweets', 'Sweets'),
    ('Snacks', 'Snacks'),
]

# Filter Choices
PICKLE_TYPE = [
    ('Veg', 'Vegetarian'),
    ('Non-Veg', 'Non-Vegetarian'),
]

SWEET_TYPE = [
    ('Sugar', 'With Sugar'),
    ('No-Sugar', 'Sugar-Free'),
]

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='product_images/')  # Store images
    stock = models.PositiveIntegerField(default=0)
    # Filters based on category
    pickle_type = models.CharField(max_length=20, choices=[('veg', 'Vegetarian'), ('nonveg', 'Non-Vegetarian')], null=True, blank=True)
    sweet_type = models.CharField(max_length=10, choices=SWEET_TYPE, blank=True, null=True)

    def __str__(self):
        return self.name
    @property
    def is_available(self):
        return self.stock > 0

# order models
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Correct way to reference user model
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


@property
def subtotal(self):
    return self.quantity * self.price
# wishlist models

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist items

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# address models
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    street = models.CharField(max_length=255)        # make sure this exists
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, default='000000') # make sure this exists
    country = models.CharField(max_length=100)       # make sure this exists
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name}, {self.city}"
    
from django.db import models
from django.conf import settings

def user_profile_path(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=user_profile_path, blank=True, null=True)

    def __str__(self):
        return self.user.username


