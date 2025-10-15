from django.urls import path
from .views import SignUpView, LoginView, SelectBranchView, CreateBranchView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('select_branch/', SelectBranchView.as_view(), name='select_branch'),
    path('create_branch/', CreateBranchView.as_view(), name='create_branch'),
]
