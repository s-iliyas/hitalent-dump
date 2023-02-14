from django.contrib import admin

# Register your models here.
from .models import Hr


class HrAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
    ]
    list_display_links = ["email", "first_name"]


admin.site.register(Hr, HrAdmin)
