import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Loan, Borrower, LoanPayment


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['loan_count'] = Loan.objects.count()
    ctx['loan_applied'] = Loan.objects.filter(status='applied').count()
    ctx['loan_approved'] = Loan.objects.filter(status='approved').count()
    ctx['loan_disbursed'] = Loan.objects.filter(status='disbursed').count()
    ctx['loan_total_amount'] = Loan.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['borrower_count'] = Borrower.objects.count()
    ctx['borrower_active'] = Borrower.objects.filter(status='active').count()
    ctx['borrower_blacklisted'] = Borrower.objects.filter(status='blacklisted').count()
    ctx['borrower_cleared'] = Borrower.objects.filter(status='cleared').count()
    ctx['borrower_total_income'] = Borrower.objects.aggregate(t=Sum('income'))['t'] or 0
    ctx['loanpayment_count'] = LoanPayment.objects.count()
    ctx['loanpayment_bank'] = LoanPayment.objects.filter(payment_method='bank').count()
    ctx['loanpayment_cash'] = LoanPayment.objects.filter(payment_method='cash').count()
    ctx['loanpayment_upi'] = LoanPayment.objects.filter(payment_method='upi').count()
    ctx['loanpayment_total_amount'] = LoanPayment.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['recent'] = Loan.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def loan_list(request):
    qs = Loan.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(loan_id__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'loan_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def loan_create(request):
    if request.method == 'POST':
        obj = Loan()
        obj.loan_id = request.POST.get('loan_id', '')
        obj.borrower_name = request.POST.get('borrower_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.interest_rate = request.POST.get('interest_rate') or 0
        obj.tenure_months = request.POST.get('tenure_months') or 0
        obj.emi = request.POST.get('emi') or 0
        obj.status = request.POST.get('status', '')
        obj.disbursed_date = request.POST.get('disbursed_date') or None
        obj.purpose = request.POST.get('purpose', '')
        obj.save()
        return redirect('/loans/')
    return render(request, 'loan_form.html', {'editing': False})


@login_required
def loan_edit(request, pk):
    obj = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        obj.loan_id = request.POST.get('loan_id', '')
        obj.borrower_name = request.POST.get('borrower_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.interest_rate = request.POST.get('interest_rate') or 0
        obj.tenure_months = request.POST.get('tenure_months') or 0
        obj.emi = request.POST.get('emi') or 0
        obj.status = request.POST.get('status', '')
        obj.disbursed_date = request.POST.get('disbursed_date') or None
        obj.purpose = request.POST.get('purpose', '')
        obj.save()
        return redirect('/loans/')
    return render(request, 'loan_form.html', {'record': obj, 'editing': True})


@login_required
def loan_delete(request, pk):
    obj = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/loans/')


@login_required
def borrower_list(request):
    qs = Borrower.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'borrower_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def borrower_create(request):
    if request.method == 'POST':
        obj = Borrower()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.address = request.POST.get('address', '')
        obj.income = request.POST.get('income') or 0
        obj.credit_score = request.POST.get('credit_score') or 0
        obj.active_loans = request.POST.get('active_loans') or 0
        obj.status = request.POST.get('status', '')
        obj.id_number = request.POST.get('id_number', '')
        obj.save()
        return redirect('/borrowers/')
    return render(request, 'borrower_form.html', {'editing': False})


@login_required
def borrower_edit(request, pk):
    obj = get_object_or_404(Borrower, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.address = request.POST.get('address', '')
        obj.income = request.POST.get('income') or 0
        obj.credit_score = request.POST.get('credit_score') or 0
        obj.active_loans = request.POST.get('active_loans') or 0
        obj.status = request.POST.get('status', '')
        obj.id_number = request.POST.get('id_number', '')
        obj.save()
        return redirect('/borrowers/')
    return render(request, 'borrower_form.html', {'record': obj, 'editing': True})


@login_required
def borrower_delete(request, pk):
    obj = get_object_or_404(Borrower, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/borrowers/')


@login_required
def loanpayment_list(request):
    qs = LoanPayment.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(loan_id__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(payment_method=status_filter)
    return render(request, 'loanpayment_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def loanpayment_create(request):
    if request.method == 'POST':
        obj = LoanPayment()
        obj.loan_id = request.POST.get('loan_id', '')
        obj.borrower_name = request.POST.get('borrower_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.payment_date = request.POST.get('payment_date') or None
        obj.payment_method = request.POST.get('payment_method', '')
        obj.status = request.POST.get('status', '')
        obj.late_fee = request.POST.get('late_fee') or 0
        obj.remaining_balance = request.POST.get('remaining_balance') or 0
        obj.save()
        return redirect('/loanpayments/')
    return render(request, 'loanpayment_form.html', {'editing': False})


@login_required
def loanpayment_edit(request, pk):
    obj = get_object_or_404(LoanPayment, pk=pk)
    if request.method == 'POST':
        obj.loan_id = request.POST.get('loan_id', '')
        obj.borrower_name = request.POST.get('borrower_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.payment_date = request.POST.get('payment_date') or None
        obj.payment_method = request.POST.get('payment_method', '')
        obj.status = request.POST.get('status', '')
        obj.late_fee = request.POST.get('late_fee') or 0
        obj.remaining_balance = request.POST.get('remaining_balance') or 0
        obj.save()
        return redirect('/loanpayments/')
    return render(request, 'loanpayment_form.html', {'record': obj, 'editing': True})


@login_required
def loanpayment_delete(request, pk):
    obj = get_object_or_404(LoanPayment, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/loanpayments/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['loan_count'] = Loan.objects.count()
    data['borrower_count'] = Borrower.objects.count()
    data['loanpayment_count'] = LoanPayment.objects.count()
    return JsonResponse(data)
