from django.contrib import admin
from django import forms
from helpers.models import FeatureFlag


class FeatureFlagForm(forms.ModelForm):
    fields = '__all__'
    form = FeatureFlag


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    form = FeatureFlagForm
    list_display = ['title', 'value', 'changed', 'has_users']
    list_editable = ['value', ]
