from django.contrib import admin

from .models import HrLinkedInCred, Intern


class InternAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
    ]
    list_display_links = ["email", "first_name"]


admin.site.register(Intern, InternAdmin)


class HrLinkedInCredAdmin(admin.ModelAdmin):
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


admin.site.register(HrLinkedInCred, HrLinkedInCredAdmin)
