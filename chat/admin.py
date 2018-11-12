from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Message, UserPresence

admin.site.register(Message)


class UserPresenceInline(admin.StackedInline):
    model = UserPresence
    can_delete = False
    verbose_name_plural = 'presence'


class UserAdmin(BaseUserAdmin):
    inlines = (UserPresenceInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
