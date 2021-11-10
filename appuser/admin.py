from django import forms
from django.contrib import admin

from appuser.models import AppUser, Policy
from django_summernote.admin import SummernoteModelAdmin


class PolicyForm(forms.ModelForm):
    model = Policy
    fields = '__all__'


@admin.register(Policy)
class PolicyAdmin(SummernoteModelAdmin):
    form = PolicyForm
    list_display = ['version', 'current', 'created']
    list_editable = ['current']
    summernote_fields = ('privacy_policy', 'eula')


class AppUserForm(forms.ModelForm):
    model = AppUser
    fields = '__all__'


@admin.register(AppUser)
class AppUserAdmin(SummernoteModelAdmin):
    form = AppUserForm
    list_display = ['user', 'display_name', 'superuser', 'has_valid_policy']
