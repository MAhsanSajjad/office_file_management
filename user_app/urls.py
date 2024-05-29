
from django.urls import path
from user_app.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin_register', index, name='register'),
    path('user-login', user_login, name='user-login'),
    path('dashboard', dashboard, name='dashboard'),
    path('logout',logout, name='logout'),
    path('upload_file',upload_file, name='upload_file'),

    path('admin_panel_view_users/', admin_panel_view_users, name="admin_panel_view_users"),
    path('admin_panel_search_user/', admin_panel_search_user, name='admin_panel_search_user'),
    path('admin_panel_delete_user/',admin_panel_delete_user, name='admin_panel_delete_user'),
    path('admin_panel_view_active_user/', admin_panel_view_active_user, name="admin_panel_view_active_user"),
    path('admin_panel_search_active_user/', admin_panel_search_active_user, name="admin_panel_search_active_user"),
    path('admin_panel_delete_active_user/', admin_panel_delete_active_user, name="admin_panel_delete_active_user"),
    path('admin_panel_view_inactive_user/', admin_panel_view_inactive_user, name="admin_panel_view_inactive_user"),
    path('admin_panel_search_inactive_user/', admin_panel_search_inactive_user, name="admin_panel_search_inactive_user"),
    path('admin_panel_block_user/', admin_panel_block_user, name="admin_panel_block_user"),


    # password reset/forget password URL
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
    name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
    name="password_reset_confirm"),
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
    name="password_reset_complete"),

]
