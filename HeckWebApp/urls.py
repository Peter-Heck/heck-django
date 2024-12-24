from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('protected/post/', views.make_post, name='make_post'),
    path('protected/edit_profile/name', views.edit_profile_name, name='edit_profile_name'),
    path('protected/edit_profile/image', views.edit_profile_image, name='edit_profile_image'),
    path('protected/edit_profile/bio', views.edit_profile_bio, name='edit_profile_bio'),
    path('profile/<str:name>/', views.profile, name='profile'),
    path('privacy', views.privacy, name='privacy'),
    path('posts/', views.list_load_posts_view, name='posts'),
]
