from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:pk>/edit/', views.loan_edit, name='loan_edit'),
    path('loans/<int:pk>/delete/', views.loan_delete, name='loan_delete'),
    path('borrowers/', views.borrower_list, name='borrower_list'),
    path('borrowers/create/', views.borrower_create, name='borrower_create'),
    path('borrowers/<int:pk>/edit/', views.borrower_edit, name='borrower_edit'),
    path('borrowers/<int:pk>/delete/', views.borrower_delete, name='borrower_delete'),
    path('loanpayments/', views.loanpayment_list, name='loanpayment_list'),
    path('loanpayments/create/', views.loanpayment_create, name='loanpayment_create'),
    path('loanpayments/<int:pk>/edit/', views.loanpayment_edit, name='loanpayment_edit'),
    path('loanpayments/<int:pk>/delete/', views.loanpayment_delete, name='loanpayment_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
