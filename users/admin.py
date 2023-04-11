from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentUser, CustomerUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes

class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    add_fieldsets = (
        
        (None, {
            'fields': ('email', 'password1', 'password2')
        }),
        ('Персональная информация', {
            'fields': ('last_name', 'first_name', 'patronymic')
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Персональная информация', {
            'fields': ('last_name', 'first_name', 'patronymic',)
        }),
        ('Права', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Системные даты', {
            'fields': ('last_login', 'date_joined')
        }),
        

    
    )
    list_display = ("email" ,"last_name","first_name", "patronymic" )

admin.site.register(User, CustomUserAdmin)



@admin.register(StudentUser)
class StudentTypeAdmin(admin.ModelAdmin):

    list_display = ("user",)

@admin.register(CustomerUser)
class CustomerTypeAdmin(admin.ModelAdmin):

    list_display = ("user",)


