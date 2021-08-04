from django.urls import path
from .views import SignUpView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:pk>/profile/", ShowProfilePageView.as_view(), name="show_profile_page"),
    path("<int:pk>/edit-profile/", EditProfilePageView.as_view(), name="edit_profile_page"),
    path("create-profile-page/", CreateProfilePageView.as_view(), name="create_profile_page"),
]
