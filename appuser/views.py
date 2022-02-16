import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from appuser import forms

from appuser.models import (
    Policy,
    PolicyLog
)


def _login(form, request):
    form = form(request.POST)
    error = None
    result = {
        'valid': True,
        'form': None,
        'user': None,
    }
    if form.is_valid():
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = User.objects.filter(email__iexact=email).first()
        if user:
            password_check = user.check_password(password)
            if password_check:
                login(request, user)
                result['user'] = user
            else:
                error = 'Password did not match.'
        else:
            error = 'User with this email address not found.'
    else:
        error = 'Invalid form submission.'
    if error:
        result['valid'] = False
    result['form'] = form
    result['error'] = '{} Please check your information and try again'.format(error)
    return result


class Login(View):
    def setup(self, request, *args, **kwargs):
        super(Login, self).setup(request, *args, **kwargs)
        self.form = forms.LoginPasswordForm
        self.template = loader.get_template('appuser/login.html')
        self.context = {'form': None, 'error': None}

    def get(self, request, *args, **kwargs):
        if request.GET.get('id'):
            initial = {'email': request.GET.get('id')}
        else:
            initial = {}
        self.context['form'] = self.form(initial=initial)
        return HttpResponse(self.template.render(self.context, request))

    def post(self, request, *args, **kwargs):
        login_attempt = _login(self.form, request)
        if login_attempt['valid']:
            has_valid_policy = login_attempt['user'].appuser.has_valid_policy
            request.session['has_valid_policy'] = has_valid_policy
            if has_valid_policy:
                return redirect(reverse('home'))
            else:
                return redirect(reverse('policy_agreement'))
        else:
            messages.error(request, login_attempt['error'])
        self.context['form'] = login_attempt['form']
        return HttpResponse(self.template.render(self.context, request))


class Logout(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse('login'))


class PolicyAgreement(View):
    def setup(self, request, *args, **kwargs):
        super(PolicyAgreement, self).setup(request, *args, **kwargs)
        self.form = forms.PolicyForm
        self.user = request.user
        self.template = loader.get_template('appuser/policy-agreement.html')

    def get(self, request, *args, **kwargs):
        context = {'form': self.form()}
        return HttpResponse(self.template.render(context, request))

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            log = PolicyLog.fetch(request.user)
            log.policy = Policy.get_current()
            log.save()
            request.session['has_valid_policy'] = True
            return redirect(reverse('home'))
        context = {'form': self.form()}
        return HttpResponse(self.template.render(context, request))


class Register(View):
    def setup(self, request, *args, **kwargs):
        super(Register, self).setup(request, *args, **kwargs)
        use_display_name = settings.APPUSER_SETTINGS['use_display_name']
        use_human_name = settings.APPUSER_SETTINGS['use_human_name']
        if use_display_name and use_human_name:
            self.form = forms.RegisterDisplayNameGivenNameForm
        elif use_display_name and not use_human_name:
            self.form = forms.RegisterDisplayNameForm
        elif not use_display_name and use_human_name:
            self.form = forms.RegisterEmailGivenNameForm
        else:
            self.form = forms.RegisterEmailForm

        self.template = loader.get_template('appuser/register.html')
        self.context = {
            'form': None,
            'error': None,
            'useDisplayName': json.dumps(use_display_name),
            'useHumanName': json.dumps(use_human_name),
            'pageModule': 'registrationModule',
            'pageController': 'registrationController'
        }

    def get(self, request, *args, **kwargs):
        self.context['form'] = self.form()
        return HttpResponse(self.template.render(self.context, request))


class RegisterAPI(APIView):
    def post(self, request, *args, **kwargs):
        request_type = request.data['request']
        if settings.APPUSER_SETTINGS['use_display_name']:
            posted_username = request.data['display_name']
        else:
            posted_username = request.data['email'].lower()

        if request_type == 'check-id':

            email_existing = User.objects.filter(email__iexact=request.data['email'].lower()).exists()
            username_existing = User.objects.filter(username__iexact=posted_username.lower()).exists()
            status = 'ok'
            errors = []
            if email_existing:
                errors.append('Email already in use')
                status = 'error'

            if username_existing and settings.APPUSER_SETTINGS['use_display_name']:
                errors.append('Username already in use')
                status = 'error'

            response = {
                'status': status,
                'errors': errors
            }
        elif request_type == 'register':

            if settings.APPUSER_SETTINGS['use_human_name']:
                first_name = request.data['first_name']
                last_name = request.data['last_name']
            else:
                first_name = None
                last_name = None
            user = User(
                email=request.data['email'],
                username=posted_username,
                first_name=first_name,
                last_name=last_name,
            )
            try:
                user.save()
                user.set_password(request.data['password'])
                user.save()
                response = {
                    'status': 'ok'
                }
            except:
                response = {
                    'status': 'error',
                    'message': 'Unknown internal error occurred. Please try again.'
                }
        else:
            response = {
                'status': 'error',
                'message': 'Unrecognized request.'
            }

        return Response(response)


class ProfileAPI(APIView):
    def setup(self, request, *args, **kwargs):
        super(ProfileAPI, self).setup(request, *args, **kwargs)
        self.use_display_name = settings.APPUSER_SETTINGS['use_display_name']
        self.use_human_name = settings.APPUSER_SETTINGS['use_human_name']

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'user': {
                    'email': request.user.email,
                    'username': request.user.username,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name
                },
                'settings': {
                    'use_display_name': settings.APPUSER_SETTINGS['use_display_name'],
                    'use_human_name': settings.APPUSER_SETTINGS['use_human_name'],
                }
            }
        )

    def put(self, request, *args, **kwargs):
        request_type = request.data.get('request')
        if request_type == 'check-id':
            if self.use_display_name:
                posted_username = request.data['user']['display_name']
            else:
                posted_username = request.data['user']['email'].lower()

            if request.user.is_authenticated:
                email_existing = User.objects.filter(
                    email__iexact=request.data['user']['email'].lower()
                ).exclude(pk=request.user.pk).exists()
                username_existing = User.objects.filter(
                    username__iexact=posted_username.lower()
                ).exclude(pk=request.user.pk).exists()
            else:
                email_existing = User.objects.filter(email__iexact=request.data['email'].lower()).exists()
                username_existing = User.objects.filter(username__iexact=posted_username.lower()).exists()

            status = 'ok'
            errors = []

            if email_existing or username_existing:
                if email_existing:
                    errors.append('Email already in use')
                    status = 'error'

                if username_existing and settings.APPUSER_SETTINGS['use_display_name']:
                    errors.append('Username already in use')
                    status = 'error'
            else:
                request.user.email = request.data['user']['email'].lower()
                request.user.usernamr = posted_username
                if self.use_human_name:
                    request.user.first_name = request.data['user']['first_name']
                    request.user.last_name = request.data['user']['last_name']
                request.user.save()

            response = {
                'status': status,
                'errors': errors
            }
        elif request_type == 'update-password':
            current_password = request.data['current_password']
            new_password = request.data['new_password']
            password_check = request.user.check_password(current_password)
            if password_check:
                request.user.set_password(new_password)
                request.user.save()
                logout(request)
                response = {
                    'status': 'ok',
                }
            else:
                response = {
                    'status': 'error',
                    'errors': ['Provided password incorrect.']
                }
        else:
            response = {
                'status': 'error',
                'errors': ['Request not recognized']
            }

        return Response(response)


class PolicyBase(View):
    def setup(self, request, *args, **kwargs):
        super(PolicyBase, self).setup(request, *args, **kwargs)
        self.current_policy = Policy.objects.get(current=True)
        self.template = loader.get_template('appuser/policy.html')


class PrivacyPolicy(PolicyBase):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Privacy Policy',
            'header': 'GDPR PRIVACY NOTICE',
            'content': self.current_policy.privacy_policy,
            'last_updated': self.current_policy.created_display,
        }
        return HttpResponse(self.template.render(context, request))


class EULA(PolicyBase):
    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'EULA',
            'header': 'END USER LICENSE AGREEMENT',
            'content': self.current_policy.eula,
            'last_updated': self.current_policy.created_display,
        }
        return HttpResponse(self.template.render(context, request))


class UserProfile(View):
    def setup(self, request, *args, **kwargs):
        use_display_name = settings.APPUSER_SETTINGS['use_display_name']
        use_human_name = settings.APPUSER_SETTINGS['use_human_name']
        self.initial_values = {
            'email': request.user.email,
            'display_name': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        self.template = loader.get_template('appuser/profile.html')
        self.context = {
            'error': None,
            'useDisplayName': json.dumps(use_display_name),
            'useHumanName': json.dumps(use_human_name),
            'user': json.dumps(self.initial_values),
            'pageModule': 'profileModule',
            'pageController': 'profileController'
        }
        super(UserProfile, self).setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return HttpResponse(self.template.render(self.context, request))
