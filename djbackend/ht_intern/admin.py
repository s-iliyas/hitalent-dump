from django.contrib import admin

# Register your models here.
from .models import InternLinkedInCred


class InternLinkedInCredAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "email",
        "locale",
        "accessToken",
        "expires_in",
        "token_type",
        "id_token",
    ]
    list_display_links = ["id", "name", "email"]


admin.site.register(InternLinkedInCred, InternLinkedInCredAdmin)
