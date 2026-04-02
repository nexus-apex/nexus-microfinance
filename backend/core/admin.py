from django.contrib import admin
from .models import Loan, Borrower, LoanPayment

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ["loan_id", "borrower_name", "amount", "interest_rate", "tenure_months", "created_at"]
    list_filter = ["status"]
    search_fields = ["loan_id", "borrower_name"]

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "income", "credit_score", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email", "phone"]

@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ["loan_id", "borrower_name", "amount", "payment_date", "payment_method", "created_at"]
    list_filter = ["payment_method", "status"]
    search_fields = ["loan_id", "borrower_name"]
