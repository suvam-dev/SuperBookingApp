from django.db import models
from django.utils import timezone
from backend.user.models import User
from backend.booking.models import Booking


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('wallet', 'Digital Wallet'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_GATEWAY_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
    ]

    payment_reference      = models.CharField(
        max_length=100, 
        unique=True, 
        db_index=True,
        null=False,
        help_text='Transaction ID from payment gateway'
    )
    booking_id                = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment',
        unique=True,
        db_index=True
    )
    user_id            = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        db_index=True
    )
    amount                 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )
    payment_method         = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=False
    )
    status                 = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    payment_gateway        = models.CharField(
        max_length=50,
        choices=PAYMENT_GATEWAY_CHOICES,
        blank=True,
        null=True,
        help_text='Which payment gateway processed this'
    )
    gateway_transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Transaction ID from the payment gateway'
    )
    error_message          = models.TextField(
        blank=True,
        null=True,
        help_text='Error details if payment failed'
    )
    paid_at                = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the payment was successfully processed'
    )
    refunded_at            = models.DateTimeField(
        blank=True,
        null=True,
        help_text='When the payment was refunded'
    )
    created_at             = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at             = models.DateTimeField(auto_now=True)

    def mark_success(self):
        """Mark payment as successful."""
        self.status = 'success'
        self.paid_at = timezone.now()
        self.save()

    def mark_failed(self, error_msg=None):
        """Mark payment as failed with optional error message."""
        self.status = 'failed'
        self.error_message = error_msg
        self.save()

    def mark_refunded(self):
        """Mark payment as refunded."""
        self.status = 'refunded'
        self.refunded_at = timezone.now()
        self.save()

    def is_successful(self):
        return self.status == 'success'

    def is_failed(self):
        return self.status == 'failed'

    def is_refunded(self):
        return self.status == 'refunded'

    def __str__(self):
        return f"Payment {self.payment_reference} - {self.status}"

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['created_at']),
        ]