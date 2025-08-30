from django.db import models

# Create your models here.

class Payment(models.Model):
    cardholder_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_intent_id = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cardholder_name} - EUR €{self.amount}"

    class Meta:
        ordering = ['-created_at']
