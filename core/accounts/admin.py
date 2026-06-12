from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, CustomerProfile

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["id","email","type","is_staff","is_active"]
    list_display_links = ["id","email"]
    list_filter = ["type","is_staff","is_active"]
    search_fields = ["id","email"]
    ordering = ("id",)

    fieldsets = (
        ("Authentication",{
            "fields":("email","password"),
        }),
        ("Permissions",{
            "fields":("type","is_superuser","is_staff","is_active"),
        }),
        ("Group Permissions",{
            "fields":("groups","user_permissions"),
        }),
        ("Important Date",{
            "fields":("last_login",),
        }),
    )

    add_fieldsets = (
        (None,{
            "classes":("wide"),
            "fields":("email","password1","password2","type","is_staff","is_active"),
        }),
    )


class CustomerProfileAdmin(admin.ModelAdmin):
    model = CustomerProfile
    list_display = ["id","user","first_name","last_name","phone_number"]
    list_display_links = ["id","user"]
    search_fields = ["user","first_name","last_name"]


admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(User, CustomUserAdmin)