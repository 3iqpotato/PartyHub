from PartyHub_Project.Accounts.forms import UserProfileEditForm, UserProfileCreateForm
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    form = UserProfileEditForm
    add_form = UserProfileCreateForm
    list_display = ('username', 'email', 'get_parties_count', 'points')

    @staticmethod
    def get_parties_count(obj):
        return obj.organized_parties.count()

    add_fieldsets = (
        (
            'Create UserProfile',
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        ('Credentials', {'fields': ('email', 'first_name', 'last_name')}),
        ('Main information',
         {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions', 'points',)}),
        ('Last Online', {'fields': ('last_login',)})
    )
