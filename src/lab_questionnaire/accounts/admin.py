from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser


class MyUserAdmin(UserAdmin):
    list_display = ('student_number', 'is_active', 'is_staff', 'is_superuser', 'gpa', 'first_choice', 'password')
    add_fieldsets = (
        (None, {
            'fields': (
                'student_number', 'is_active', 'is_staff', 'is_superuser',
                'gpa', 'first_choice',
                'password1', 'password2'
            )
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('student_number', 'is_active', 'is_staff', 'is_superuser', 'gpa', 'first_choice', 'password')
        }),
    )
    ordering = ('student_number',)


admin.site.register(MyUser, MyUserAdmin)
