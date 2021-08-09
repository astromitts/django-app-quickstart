from django.forms import (
    BooleanField,
    CharField,
    CheckboxInput,
    EmailInput,
    Form,
    PasswordInput,
)
from django.utils.safestring import mark_safe


class PolicyForm(Form):
    eula = BooleanField(
        widget=CheckboxInput(),
        label=mark_safe(
            'I have read and agree to the <a href="/user/eula/">End User License Agreement</a>'
        ),
        required=True
    )
    pp = BooleanField(
        widget=CheckboxInput(),
        label=mark_safe(
            'I have read and agree to the <a href="/user/privacy-policy/">Privacy Policy</a>'
        ),
        required=True
    )


class LoginPasswordForm(Form):
    email = CharField(widget=EmailInput(attrs={'class': 'form-control'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(Form):
    email = CharField(widget=EmailInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'ng-model': 'email'
    }))
    password = CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'ng-model': 'newPassword'
    }))
    confirm_password = CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'ng-model': 'confirmPassword'
    }))
