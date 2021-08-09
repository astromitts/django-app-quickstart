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

from appuser.forms import (
    LoginPasswordForm,
    PolicyForm,
    RegisterForm,
)

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
        username = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = User.objects.filter(username__iexact=username).first()
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
        self.form = LoginPasswordForm
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
        self.form = PolicyForm
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
        self.form = RegisterForm
        self.template = loader.get_template('appuser/register.html')
        self.context = {
            'form': None,
            'error': None,
            'pageModule': 'registrationModule',
            'pageController': 'registrationController'
        }

    def get(self, request, *args, **kwargs):
        self.context['form'] = self.form()
        return HttpResponse(self.template.render(self.context, request))


class RegisterAPI(APIView):
    def post(self, request, *args, **kwargs):
        request_type = request.data['request']
        if request_type == 'check-id':
            email_existing = User.objects.filter(email__iexact=request.data['email'].lower()).exists()
            status = 'ok'
            errors = []
            if email_existing:
                errors.append('Email already in use')
                status = 'error'
            response = {
                'status': status,
                'errors': errors
            }
        elif request_type == 'register':
            user = User(
                email=request.data['email'],
                username=request.data['email']
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
