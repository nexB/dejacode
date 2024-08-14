#
# Copyright (c) nexB Inc. and others. All rights reserved.
# DejaCode is a trademark of nexB Inc.
# SPDX-License-Identifier: AGPL-3.0-only
# See https://github.com/aboutcode-org/dejacode for support or download.
# See https://aboutcode.org for more information about AboutCode FOSS projects.
#

"""
Two-factor authentication in DejaCode.

Two-factor is implemented using the TOTP protocol (Time-based One-Time Password).
The `django_otp` library is used for the models (`TOTPDevice`) and
low-level functionality.

This implementation consist in 2 views:
 - Enable 2FA with `two_factor.EnableView`
 - Disable 2FA with `two_factor.DisableView`
Plus an extra verification step during login when 2FA is enabled:
 - `two_factor.LoginView` + `two_factor.VerifyView`

When a user has enabled 2FA, he will have to provide a valid `token`,
generated by his mobile device, following his `username` and `password`,
during the login process.
"""

from contextlib import suppress
from io import BytesIO

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.db import models
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

import django_otp
import qrcode
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from crispy_forms.layout import Field
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.forms import OTPTokenForm
from django_otp.oath import TOTP
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.models import default_key
from qrcode.image.svg import SvgPathImage

from dje.models import DejacodeUser

TWOFA_USER_SESSION_KEY = "_2fa_user_id"


class TwoFactorEnableForm(OTPAuthenticationFormMixin, forms.Form):
    """
    Verify the validity of the user provided `token`.
    Create a 'default' TOTPDevice on save.
    """

    token = forms.IntegerField(
        label=_("Token"),
        min_value=0,
        max_value=999999,
    )

    def __init__(self, user, key, *args, **kwargs):
        self.user = user
        self.key = key
        super().__init__(*args, **kwargs)

    @property
    def bin_key(self):
        """Return the secret key as a binary string."""
        return TOTPDevice(key=self.key).bin_key

    def clean_token(self):
        """Verify the validity of the provided `token`."""
        token = self.cleaned_data.get("token")

        if not token:
            raise forms.ValidationError(
                self.otp_error_messages["token_required"],
                code="token_required",
            )

        verified = TOTP(self.bin_key).verify(token, tolerance=1)

        if verified:
            return token

        raise forms.ValidationError(
            self.otp_error_messages["invalid_token"],
            code="invalid_token",
        )

    def save(self):
        return TOTPDevice.objects.create(
            user=self.user,
            key=self.key,
            name="default",
        )

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = "2fa_enable"
        helper.form_show_labels = False

        fields = [
            Field(
                "token",
                css_class="input-block-level",
                placeholder=_("Authentication token"),
                autofocus=True,
            ),
            Div(
                Submit("submit", _("Enable two-factor")),
                css_class="d-grid",
            ),
        ]
        helper.add_layout(Layout(Fieldset("", *fields)))

        return helper


class TwoFactorDisableForm(OTPTokenForm):
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = "2fa_disable"
        helper.form_show_labels = False

        fields = [
            Field("otp_device", css_class="d-none"),
            Field(
                "otp_token",
                css_class="input-block-level",
                placeholder=_("Authentication token"),
                autofocus=True,
            ),
            Div(
                Submit(
                    "submit",
                    _("Disable two-factor"),
                    css_class="btn-danger",
                ),
                css_class="d-grid",
            ),
        ]
        helper.add_layout(Layout(Fieldset("", *fields)))

        return helper


class TwoFactorVerifyForm(OTPTokenForm):
    """Verify that the user provided `otp_token` is valid."""

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = "2fa_verify"
        helper.form_show_labels = False

        fields = [
            Field("otp_device", css_class="d-none"),
            Field(
                "otp_token",
                css_class="input-block-level",
                placeholder=_("Authentication token"),
                autofocus=True,
            ),
            Div(
                Submit("submit", _("Verify")),
                css_class="d-grid",
            ),
        ]
        helper.add_layout(Layout(Fieldset("", *fields)))

        return helper


class EnableView(
    LoginRequiredMixin,
    FormView,
):
    """Enable two-factor authentication for current user."""

    template_name = "account/2fa_enable.html"
    form_class = TwoFactorEnableForm
    success_url = reverse_lazy("account_profile")
    session_key_name = "2fa_enable_key"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Redirect if two-factor is already enabled."""
        two_factor_enabled = django_otp.user_has_device(self.request.user)
        if two_factor_enabled:
            return redirect(self.get_success_url())

        return super().get(request, *args, **kwargs)

    def get_key(self):
        """Return the 2FA key from the session if available or generate a new one."""
        session = self.request.session

        if self.session_key_name in session:
            return session.get(self.session_key_name)

        new_key = default_key()
        session[self.session_key_name] = new_key

        return new_key

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "user": self.request.user,
                "key": self.get_key(),
            }
        )
        return kwargs

    def get_qr_code(self):
        """
        Return a QR code containing all the data required to enable 2FA:
        the private key, the protocol details, and the issuer.
        This QR code is scanned by an authenticator app from the user mobile
        device.
        Once scanned, the app will be able to generate a token that is used
        as second-factor for authentication.

        The QR code is generated using the `qrcode` library.
        We use the SVG format and convert the binary output into a string.
        This output can be used as-is in a HTML view as it's wrapped in
        an <svg> tag that can be interpreted by any modern browser to display
        an image.
        """
        key = self.get_key()
        device = TOTPDevice(key=key, user=self.request.user)
        config_url = device.config_url

        qr_code_bytes = BytesIO()
        image = qrcode.make(config_url, image_factory=SvgPathImage)
        image.save(qr_code_bytes)
        qr_code_svg = qr_code_bytes.getvalue().decode("utf-8")

        return qr_code_svg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "qr_code": self.get_qr_code(),
            }
        )
        return context

    def form_valid(self, form):
        """
        Create a TOTPDevice instance in the database and
        Remove the key used for enabling 2FA from the session.
        """
        form.save()
        messages.success(self.request, "Two-factor authentication enabled")

        with suppress(KeyError):
            del self.request.session[self.session_key_name]

        return super().form_valid(form)


class LoginView(DefaultLoginView):
    """
    Add the 2FA verification step in the Login process when 2FA is enable
    for the current user.
    """

    def form_invalid(self, form):
        if domain_redirect := settings.DATASPACE_DOMAIN_REDIRECT:
            if username := form.cleaned_data.get("username"):
                if user := DejacodeUser.objects.get_or_none(username=username):
                    if redirect_url := domain_redirect.get(user.dataspace.name):
                        return HttpResponseRedirect(redirect_url)
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.get_user()
        two_factor_enabled = django_otp.user_has_device(user)
        is_verified = getattr(user, "is_verified", bool)

        if two_factor_enabled and not is_verified():
            session = self.request.session
            session[TWOFA_USER_SESSION_KEY] = user.id
            session[BACKEND_SESSION_KEY] = user.backend
            return HttpResponseRedirect(reverse("account_2fa_verify"))

        return super().form_valid(form)


class VerifyView(DefaultLoginView):
    """Verify the two-factor code as a second step of the login process."""

    form_class = TwoFactorVerifyForm
    template_name = "account/2fa_verify.html"
    redirect_authenticated_user = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        user_id = self.request.session.get(TWOFA_USER_SESSION_KEY)
        if not user_id:
            raise Http404

        try:
            user = get_user_model().objects.get(id=user_id)
        except models.ObjectDoesNotExist:
            raise Http404

        kwargs.update(
            {
                "user": user,
            }
        )

        return kwargs

    def form_valid(self, form):
        """
        Run the Django's login() logic to persist the user in the session.
        Clean the session from the 2FA validation step entry.
        """
        user = form.get_user()
        session = self.request.session
        backend = session.get(BACKEND_SESSION_KEY)

        # `django_otp.login()` will be called as well through the
        # `user_logged_in` signal.
        django_auth_login(self.request, user, backend)

        with suppress(KeyError):
            del session[TWOFA_USER_SESSION_KEY]

        return HttpResponseRedirect(self.get_success_url())


class DisableView(
    LoginRequiredMixin,
    FormView,
):
    """Disable two-factor for current user."""

    template_name = "account/2fa_disable.html"
    success_url = reverse_lazy("account_profile")
    form_class = TwoFactorDisableForm

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Redirect if two-factor is not enabled."""
        two_factor_enabled = django_otp.user_has_device(self.request.user)
        if not two_factor_enabled:
            return redirect(self.get_success_url())

        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "user": self.request.user,
            }
        )
        return kwargs

    def form_valid(self, form):
        """Delete all registered devices for current user then redirects."""
        for device in django_otp.devices_for_user(self.request.user):
            device.delete()

        messages.success(self.request, "Two-factor authentication disabled")

        return super().form_valid(form)
