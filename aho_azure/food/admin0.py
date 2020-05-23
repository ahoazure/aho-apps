from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

from django.contrib.admin.models import LogEntry

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from .models import CustomUser, CustomGroup,AhodctUserLogs
from . import models
from common_info.admin import (OverideImportExport, OverideExport,
    OverideExportAdmin)
from django.forms import TextInput,Textarea #for customizing textarea row and column size


@admin.register(models.CustomUser)
class UserAdmin (UserAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    readonly_fields = ('last_login','date_joined',)

    fieldsets = (
        ('Personal info', {'fields': ('title','first_name', 'last_name',
            'gender','location')}),
        ('Login Credentials', {'fields': ('email', 'username','password',)}),
        ('Account Permissions', {'fields': ('is_active', 'is_staff',
            'is_superuser', 'groups', 'user_permissions')}),
        ('Login Details', {'fields': ('last_login',)}),
    )

    limited_fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name','location')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    list_display = ['first_name','last_name','username','email','gender',
        'location','date_joined','last_login']
    list_display_links = ['first_name','last_name','username','email']

class GroupInline(admin.StackedInline):
    model = CustomGroup
    can_delete = False
    verbose_name_plural = 'Group Roles'


admin.site.unregister(Group) # Must unregister the group in order to use the custom one
@admin.register(models.CustomGroup)
class GroupAdmin(BaseGroupAdmin):
    #inlines = (GroupInline, )
    list_display = ['name','location','roles_manager']


# This is the admin interface that allows the super admin to track user activities!
@admin.register(AhodctUserLogs)
class AhoDCT_LogsAdmin(OverideExport):
    def has_delete_permission(self, request, obj=None): #This function removes the add button on the admin interface
        return False

    def has_add_permission(self, request, obj=None): #This function removes the add button on the admin interface
        return False
    #This method removes the save buttons from the model form
    def changeform_view(self,request,object_id=None, form_url='',extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(AhoDCT_LogsAdmin, self).changeform_view(
            request, object_id, extra_context=extra_context)

    list_display=['username','email','first_name', 'last_name','location',
        'app_label','record_name','action','action_time','last_login',]
    readonly_fields = ('username','email','first_name', 'last_name','location',
        'app_label','record_name','action','action_time','last_login',)
    search_fields = ('username','email','first_name', 'last_name','location',
        'app_label','record_name','action',)

    list_filter = (
        ('record_name', DropdownFilter,),
        ('app_label', DropdownFilter,),
        ('location', DropdownFilter,),
        ('action', DropdownFilter),
    )
    ordering = ('-action_time',)
