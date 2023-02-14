from django.db import models
from django.utils import timezone

# Create your models here.
class Hr(models.Model):
    first_name = models.CharField(max_length=1000, null=True, blank=True)
    last_name = models.CharField(max_length=1000, null=True, blank=True)
    email = models.EmailField(max_length=1000, null=True, blank=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=3000, null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now, editable=False)
    updated_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "hr"

    def __str__(self):
        return self.email