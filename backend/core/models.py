from django.db import models

class Loan(models.Model):
    loan_id = models.CharField(max_length=255)
    borrower_name = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tenure_months = models.IntegerField(default=0)
    emi = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("applied", "Applied"), ("approved", "Approved"), ("disbursed", "Disbursed"), ("closed", "Closed"), ("defaulted", "Defaulted")], default="applied")
    disbursed_date = models.DateField(null=True, blank=True)
    purpose = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.loan_id

class Borrower(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    address = models.TextField(blank=True, default="")
    income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_score = models.IntegerField(default=0)
    active_loans = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("blacklisted", "Blacklisted"), ("cleared", "Cleared")], default="active")
    id_number = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class LoanPayment(models.Model):
    loan_id = models.CharField(max_length=255)
    borrower_name = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[("bank", "Bank"), ("cash", "Cash"), ("upi", "UPI"), ("auto_debit", "Auto Debit")], default="bank")
    status = models.CharField(max_length=50, choices=[("paid", "Paid"), ("overdue", "Overdue"), ("partial", "Partial")], default="paid")
    late_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.loan_id
