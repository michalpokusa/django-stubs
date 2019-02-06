from typing import Any, Dict, Optional, Set, Type, Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDict
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

UserModel: Any

class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts: Any = ...
    def get_success_url_allowed_hosts(self) -> Set[str]: ...

class LoginView(SuccessURLAllowedHostsMixin, FormView):
    form_class: Any = ...
    authentication_form: Any = ...
    redirect_field_name: Any = ...
    template_name: str = ...
    redirect_authenticated_user: bool = ...
    extra_context: Any = ...
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_success_url(self) -> str: ...
    def get_redirect_url(self) -> str: ...
    def get_form_class(self) -> Type[AuthenticationForm]: ...
    def get_form_kwargs(self) -> Dict[str, Optional[Union[Dict[str, str], HttpRequest, MultiValueDict]]]: ...
    def form_valid(self, form: AuthenticationForm) -> HttpResponseRedirect: ...
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]: ...

class LogoutView(SuccessURLAllowedHostsMixin, TemplateView):
    next_page: Any = ...
    redirect_field_name: Any = ...
    template_name: str = ...
    extra_context: Any = ...
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def post(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> TemplateResponse: ...
    def get_next_page(self) -> Optional[str]: ...
    def get_context_data(self, **kwargs: Any): ...

def logout_then_login(request: HttpRequest, login_url: Optional[str] = ...) -> HttpResponseRedirect: ...
def redirect_to_login(
    next: str, login_url: Optional[str] = ..., redirect_field_name: Optional[str] = ...
) -> HttpResponseRedirect: ...

class PasswordContextMixin:
    extra_context: Any = ...
    def get_context_data(self, **kwargs: Any): ...

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name: str = ...
    extra_email_context: Any = ...
    form_class: Any = ...
    from_email: Any = ...
    html_email_template_name: Any = ...
    subject_template_name: str = ...
    success_url: Any = ...
    template_name: str = ...
    title: Any = ...
    token_generator: Any = ...
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def form_valid(self, form: PasswordResetForm) -> HttpResponseRedirect: ...

INTERNAL_RESET_URL_TOKEN: str
INTERNAL_RESET_SESSION_TOKEN: str

class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name: str = ...
    title: Any = ...

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class: Any = ...
    post_reset_login: bool = ...
    post_reset_login_backend: Any = ...
    success_url: Any = ...
    template_name: str = ...
    title: Any = ...
    token_generator: Any = ...
    validlink: bool = ...
    user: Any = ...
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_user(self, uidb64: str) -> Optional[AbstractBaseUser]: ...
    def get_form_kwargs(self) -> Dict[str, Optional[Union[Dict[Any, Any], AbstractBaseUser, MultiValueDict]]]: ...
    def form_valid(self, form: SetPasswordForm) -> HttpResponseRedirect: ...
    def get_context_data(self, **kwargs: Any): ...

class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name: str = ...
    title: Any = ...
    def get_context_data(self, **kwargs: Any): ...

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class: Any = ...
    success_url: Any = ...
    template_name: str = ...
    title: Any = ...
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_form_kwargs(self) -> Dict[str, Optional[Union[Dict[Any, Any], User, MultiValueDict]]]: ...
    def form_valid(self, form: PasswordChangeForm) -> HttpResponseRedirect: ...

class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name: str = ...
    title: Any = ...
    def dispatch(self, *args: Any, **kwargs: Any) -> TemplateResponse: ...
