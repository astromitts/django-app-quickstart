from django.forms import (
    BooleanField,
    CharField,
    CheckboxInput,
    EmailInput,
    Form,
    PasswordInput,
    TextInput,
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


class RegisterDisplayNameForm(Form):
    email = CharField(widget=EmailInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'ng-model': 'email'
    }))
    display_name = CharField(
        help_text='How other users will identify you on the site',
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'ng-model': 'displayName',
            }
        )
    )
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


class RegisterDisplayNameGivenNameForm(Form):
    email = CharField(widget=EmailInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'ng-model': 'email'
    }))

    first_name = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'ng-model': 'firstName',
            }
        )
    )

    last_name = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'ng-model': 'lastName',
            }
        )
    )

    display_name = CharField(
        help_text='How other users will identify you on the site',
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'ng-model': 'displayName',
            }
        )
    )
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


class RegisterEmailForm(Form):
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


class RegisterEmailGivenNameForm(Form):
    email = CharField(widget=EmailInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'ng-model': 'email'
    }))

    first_name = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'ng-model': 'firstName',
            }
        )
    )

    last_name = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'ng-model': 'lastName',
            }
        )
    )
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
