from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib import auth, messages
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from apps.models import *

from logging.handlers import TimedRotatingFileHandler
import logging
logger=logging.getLogger()
logging.basicConfig(
        handlers=[ TimedRotatingFileHandler('logs.log', when="midnight", interval=1)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')


def app_registration(request, appslug):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    context = {
        'username': username,
        'email': email,
        'slug': appslug
    }
    if not User.objects.filter(username=username).exists():
        if not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request, 'Password is too short')
                return render(request, 'register.html')

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.save()

            profile = Profile.objects.get(user=user)
            profile.apps.add(applists.objects.get(slug=appslug))
            messages.success(
                request, 'Account successfully created! Check your Email for Account Activation')
            return redirect('add-customer-form', appslug)

        messages.warning(request, "This Email already exists!")
        return render(request, 'register.html', context)
    else:
        messages.warning(request, "This username already exists!")
        return render(request, 'register.html', context)

class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html', {'slug': appslug})

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'username': username,
            'email': email,
            'slug': appslug
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, 'register.html')

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                            'uidb64': uidb64, 'token': token_generator.make_token(user)})
                email_subject="Activate your Account"
                activate_url = 'http://'+domain+link
                email_body = 'Hi, ' + user.username + \
                    ' Please use this link to verify your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'from@example.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(
                    request, 'Account successfully created! Check your Email for Account Activation')
                return redirect('add-customer-form', appslug)

            messages.warning(request, "This Email already exists!")
            return render(request, 'register.html', context)
        else:
            messages.warning(request, "This username already exists!")
            return render(request, 'register.html', context)

class VerificationView(View):
    def get(self, request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            auth.login(request, user,
                    backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return render(request, 'login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        if 'login_page' in request.POST:
            next = request.POST.get('next')
            username = request.POST['username']
            password = request.POST['password']
            context = {
                'user_found': True,
                'user_name': username
            }
            if username and password:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(
                        username=username, password=password)
                    if user:
                        if user.is_active:
                            auth.login(request, user)
                            is_customer=Profile.objects.get(user=user).admin
                            if is_customer:
                                messages.success(request,"loggedin succesfully")
                                return redirect("showapps")
                            else:
                                messages.success(request,"loggedin succesfully")
                                return redirect("custdash")

                        messages.error(
                            request, "Account is not active,please check your email"
                        )

                elif User.objects.filter(email=username).exists():
                    user = User.objects.get(email=username)
                    user = auth.authenticate(
                        username=user.username, password=password)
                    if user:
                        if user.is_active:
                            auth.login(request, user)
                            is_admin=Profile.objects.get(user=user).admin
                            if is_admin:
                                messages.success(request,"loggedin succesfully")
                                return redirect("showapps")
                            else:
                                messages.success(request,"loggedin succesfully")
                                return redirect("custdash")

                        messages.error(
                            request, "Account is not active,please check your email"
                        )
                elif (User.objects.filter(email=username).exists() or User.objects.filter(username=username).exists() == False):
                    messages.warning(
                        request, "The username or Email you have entered does not exist.")
                    return render(request, 'login.html', context)

            context = {
                'user_found': True,
                'user_name': username
            }
            messages.warning(request, 'Invalid credentials, try again')
            return render(request, 'login.html', context)

        return render(request, "login.html")

def logout(request):
    logger.info(request.user.username+"_ logged out")
    auth.logout(request)
    return redirect('index')

from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from .utils import token_generator

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

from .forms import PasswordResetForm

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

from decimal import Context
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User, auth
from django.views.generic import UpdateView, DetailView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from plans.forms import UpdateUserPlanForm
from .models import Profile
from .forms import ProfileForm
from dashboard.forms import *
from .forms import *

# Create your views here.
def update_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        ph_num = request.POST.get('ph_no')

        profile.full_name = full_name
        profile.email = email
        profile.ph_num = ph_num

        profile.save()
        logger.info(request.user.username+"_ updated profile")
        return HttpResponseRedirect(reverse('show_profile', kwargs={'slug':slug}))
    else:
        if request.user == profile.user:
            return render(request, 'editprofile.html', {'profile': profile})
        else:
            return HttpResponse('siggu undali....')

class UpdateProfile(UpdateView):
    model = Profile
    template_name = 'editprofile.html'
    form_class = ProfileForm
    success_url = '/'

class ShowProfile(DetailView):
    model = Profile
    template_name = 'myprofile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfile, self).get_context_data(*args, **kwargs)
        page_profile = get_object_or_404(Profile, slug=self.kwargs['slug'])
        context['profile'] = page_profile
        context['form'] = UpdateProfilePlanForm(appslug=self.kwargs['appslug'], profile=page_profile)
        context['plan'] = page_profile.plans.filter(app__slug=self.kwargs['appslug']).first()
        context['notification_form'] = NotificationForm()
        context['appslug'] = self.kwargs['appslug']
        if self.request.user==page_profile.user:
            self.template_name = 'myprofile.html'
        elif self.request.user!=page_profile.user or self.request.user.is_anonymous:
            self.template_name = 'myprofile.html'
        return context

def create_notification(request, slug):
    profile = Profile.objects.get(user=request.user)
    form = NotificationForm(request.POST, request.FILES)
    if form.is_valid():
        url = 'https://url.com/some-url/'
        notification = form.save(commit=False)
        notification.profile = profile
        notification.url = url
        notification.save(update_fields=['profile', 'url'])
        return redirect('show_profile', slug=profile.slug, appslug=slug)
    print(form.errors)
    return redirect('show_profile', slug=profile.slug, appslug=slug)