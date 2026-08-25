from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "SoftDesk",
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                    "created_time",
                    "is_anonymized",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "SoftDesk",
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                    "email",
                    "is_anonymized",
                    "created_time",
                )
            },
        ),
    )

    readonly_fields = UserAdmin.readonly_fields + (
        "created_time",
        "is_anonymized",
    )


admin.site.register(User, CustomUserAdmin)
