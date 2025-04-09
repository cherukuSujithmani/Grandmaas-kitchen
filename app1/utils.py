from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# app1/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(user, order):
    subject = "Order Confirmation - Grandma's Kitchen"
    message = f"Hi {user.username},\n\nThank you for your order #{order.id}!\n\nTotal: ₹{order.total_price}\n\nYour items will be shipped to:\n{order.address}\n\nPayment Method: {order.payment_method}\n\nWe hope you enjoy our products!\n\n- Grandma's Kitchen"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

