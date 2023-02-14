from django.db import models
from django.utils import timezone

# Create your models here.
class Intern(models.Model):
    first_name = models.CharField(max_length=1000, null=True, blank=True)
    last_name = models.CharField(max_length=1000, null=True, blank=True)
    email = models.EmailField(max_length=1000, null=True, blank=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=3000, null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now, editable=False)
    updated_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = "interns"

    def __str__(self):
        return self.email

class HrLinkedInCred(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    locale = models.CharField(max_length=1000, null=True, blank=True)
    accessToken = models.TextField(max_length=1000, null=True, blank=True)
    expires_in = models.CharField(max_length=1000, null=True, blank=True)
    token_type = models.CharField(max_length=1000, null=True, blank=True)
    id_token = models.TextField(max_length=1000, null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now, editable=False)
    updated_time = models.DateTimeField(auto_now=True, blank=True)
    class Meta:
        db_table = "hr_linkedin_cred"

    def __str__(self):
        return self.email
