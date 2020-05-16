import os

from django.contrib.auth import login, logout as dj_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, TemplateView, DetailView

from common.consts import OBJECT_STATUS_ACTIVE, OBJECT_STATUS_INACTIVE
from crm.forms import RegistrationForm, EmailAuthenticationForm, UserDataForm, AvatarForm
from crm.tasks import send_verification_email
from crm.tokens import account_activation_token


class RegisterFormView(FormView):
    form_class = RegistrationForm
    success_url = reverse_lazy('confirm')
    template_name = os.path.join('registration', 'register.html')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.profile.birthday = form.cleaned_data["birthday"]
        user.save()

        domain = get_current_site(self.request).domain
        send_verification_email.delay(user.pk, domain)
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(LoginView):
    form_class = EmailAuthenticationForm
    success_url = reverse_lazy('profile')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data_form'] = UserDataForm(instance=self.request.user,
                                                 initial={"birthday": self.request.user.profile.birthday})
        context['avatar_form'] = AvatarForm()
        return context

    def post(self, request, **kwargs):
        udf = UserDataForm(request.POST, instance=request.user)
        if udf.is_valid():
            usr = udf.save()
            usr.profile.birthday = udf.cleaned_data['birthday']
            usr.profile.save()
        return redirect(reverse_lazy('profile'))


class GuestProfileView(DetailView):
    template_name = "guest_profile.html"
    model = User
    context_object_name = 'user'
    queryset = User.objects.filter(profile__status=OBJECT_STATUS_ACTIVE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data_form'] = UserDataForm(instance=self.request.user,
                                                 initial={"birthday": self.request.user.profile.birthday})
        return context

    def get(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().pk:
            return redirect(reverse_lazy("profile"))
        return super().get(request, *args, **kwargs)


class ActivateView(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.profile.status = OBJECT_STATUS_ACTIVE
            user.save()
            user.profile.save()
            login(request, user)
            return redirect(reverse('confirm-success'))
        else:
            user.is_active = False
            user.profile.status = OBJECT_STATUS_INACTIVE
            user.save()
            user.profile.save()
            return redirect(reverse('confirm-fail'))


class EmailConfirmationSuccessView(TemplateView):
    template_name = "message.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Вы успешно подтвердили ваш email"
        return context


class EmailConfirmationFailView(TemplateView):
    template_name = "message.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Ссылка активации невалидна"
        return context


class EmailConfirmationView(TemplateView):
    template_name = "message.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Подтвердите, пожалуйста, ваш email"
        return context


class AvatarUploadView(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        af = AvatarForm(request.POST, request.FILES, instance=request.user.profile)
        if af.is_valid():
            af.save()
        return redirect(reverse_lazy('profile'))



def logout(request):
    dj_logout(request)
    return redirect(reverse_lazy('index'))
