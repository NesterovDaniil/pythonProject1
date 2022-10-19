from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import ChangeUserInfoForm
from .models import AdvUser
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView

from .forms import RegisterUserForm

from django.views.generic.base import TemplateView


def index(request):
    return render(request, 'main/index.html')


class BBLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

    class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,
                             UpdateView):
        model = AdvUser
        template_name = 'main/change_user_info.html'
        form_class = ChangeUserInfoForm
        success_url = reverse_lazy('main:profile')
        success_message = 'Личные данные пользователя изменены'

        def __init__(self, **kwargs):
            super().__init__(kwargs)
            self.user_id = None

        def dispatch(self, request, *args, **kwargs):
            self.user_id = request.user.pk
            return super().dispatch(request, *args, **kwargs)

        def get_object(self, queryset=None):
            if not queryset:
                queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                           PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


class ChangeUserInfoView(CreateView):
    pass


from django.core.signing import BadSignature
from .utilities import signer


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_activated = True
        user.is_active = True
        user.save()
    return render(request, template)


from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth import logout
from django.contrib import messages


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)



#СОЗДАНИЕ ЗАЯВКИ
#from django.views.generic.edit import CreateView
#from .models import GeeksModel


#class GeeksCreate(CreateView):
    # specify the model for create view
#    model = GeeksModel

    # specify the fields to be displayed

 #   fields = ['title', 'description']