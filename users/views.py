from core_app.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "profile/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        context["page_user"] = page_user
        return context


class EditProfilePageView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile/edit_profile_page.html"
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "bio",
        "profile_pic",
        "facebook_url",
        "instagram_url",
        "twitter_url",
    ]
    success_url = reverse_lazy("post_list")


class CreateProfilePageView(CreateView):
    model = Profile
    template_name = "profile/create_profile_page.html"
    success_url = reverse_lazy("post_list")
    fields = [
        "first_name",
        "last_name",
        "username",
        "email",
        "bio",
        "profile_pic",
        "facebook_url",
        "instagram_url",
        "twitter_url",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
