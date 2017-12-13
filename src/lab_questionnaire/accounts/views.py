import re
from django.views.generic import TemplateView, UpdateView, ListView, FormView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django import forms
from .models import MyUser
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import Http404


class RegisterForm(UserCreationForm):
    student_number = forms.CharField(label="学生ID (情報科学センターのログインID。メール認証に用います。）")

    def clean(self):
        cleansed_data = super(RegisterForm, self).clean()
        cleansed_student_number = cleansed_data.get("student_number")
        match_obj = re.match(r"^(b|m)\d{7}$", cleansed_student_number)
        if match_obj is None:
            raise ValidationError("学生IDが不正です。例: b2122044")

    class Meta:
        model = MyUser
        fields = ("student_number",)


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        form.instance.is_active = False
        user = form.save()
        result = super().form_valid(form)

        user = MyUser.objects.get(pk=user.pk)
        subject_template = get_template('accounts/register_subject.txt')
        message_template = get_template('accounts/register_message.txt')
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'base_uri': settings.BASE_URI,
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': default_token_generator.make_token(user),
            'user': user,
        }
        subject = subject_template.render(context)
        message = message_template.render(context)
        mail_address = form.instance.student_number + settings.EMAIL_PREFIX
        send_mail(subject, message, settings.EMAIL_ADDRESS, [mail_address])

        return result

    def get_success_url(self):
        return reverse('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'accounts/register_done.html'


class RegisterCompleteView(TemplateView):
    template_name = 'accounts/register_complete.html'

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        uid = force_text(urlsafe_base64_decode(kwargs.get('uidb64')))
        try:
            user = MyUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None

        if user and not user.is_active:
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return super().get(request, **kwargs)

        raise Http404


class MyPasswordResetForm(forms.Form):
    student_number = forms.CharField(label="学生ID")

    def clean(self):
        current_student_number = self.cleaned_data["student_number"]
        try:
            MyUser.objects.get(student_number=current_student_number)
            match_obj = re.match(r"^(b|m)\d{7}$", current_student_number)
        except ObjectDoesNotExist:
            match_obj = None
        if match_obj is None:
            raise ValidationError("該当するユーザは存在しません。")
        else:
            return current_student_number


class PasswordResetView(FormView):
    template_name = 'accounts/password_reset.html'
    form_class = MyPasswordResetForm

    def form_valid(self, form):
        result = super().form_valid(form)
        student_number = form.data.get("student_number")
        user = MyUser.objects.get(student_number=student_number)
        subject_template = get_template('accounts/password_reset_subject.txt')
        message_template = get_template('accounts/password_reset_message.txt')
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'base_uri': settings.BASE_URI,
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': default_token_generator.make_token(user),
            'user': user,
        }
        subject = subject_template.render(context)
        message = message_template.render(context)
        mail_address = user.student_number + settings.EMAIL_PREFIX
        send_mail(subject, message, settings.EMAIL_ADDRESS, [mail_address])

        return result

    def get_success_url(self):
        return reverse('password_reset_done')
