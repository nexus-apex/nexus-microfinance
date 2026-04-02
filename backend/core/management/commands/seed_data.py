from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Loan, Borrower, LoanPayment
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusMFI with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusmfi.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Loan.objects.count() == 0:
            for i in range(10):
                Loan.objects.create(
                    loan_id=f"Sample {i+1}",
                    borrower_name=f"Sample Loan {i+1}",
                    amount=round(random.uniform(1000, 50000), 2),
                    interest_rate=round(random.uniform(1000, 50000), 2),
                    tenure_months=random.randint(1, 100),
                    emi=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["applied", "approved", "disbursed", "closed", "defaulted"]),
                    disbursed_date=date.today() - timedelta(days=random.randint(0, 90)),
                    purpose=f"Sample purpose for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Loan records created'))

        if Borrower.objects.count() == 0:
            for i in range(10):
                Borrower.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    address=f"Sample address for record {i+1}",
                    income=round(random.uniform(1000, 50000), 2),
                    credit_score=random.randint(1, 100),
                    active_loans=random.randint(1, 100),
                    status=random.choice(["active", "blacklisted", "cleared"]),
                    id_number=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Borrower records created'))

        if LoanPayment.objects.count() == 0:
            for i in range(10):
                LoanPayment.objects.create(
                    loan_id=f"Sample {i+1}",
                    borrower_name=f"Sample LoanPayment {i+1}",
                    amount=round(random.uniform(1000, 50000), 2),
                    payment_date=date.today() - timedelta(days=random.randint(0, 90)),
                    payment_method=random.choice(["bank", "cash", "upi", "auto_debit"]),
                    status=random.choice(["paid", "overdue", "partial"]),
                    late_fee=round(random.uniform(1000, 50000), 2),
                    remaining_balance=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 LoanPayment records created'))
