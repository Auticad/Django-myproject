"""View utenti — apps/users/views.py"""
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, ProfileForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class    = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url   = reverse_lazy('blog:post-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object,
              backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f'Benvenuto, {self.object.username}!')
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model         = CustomUser
    form_class    = ProfileForm
    template_name = 'registration/profile.html'
    success_url   = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profilo aggiornato.')
        return super().form_valid(form)
