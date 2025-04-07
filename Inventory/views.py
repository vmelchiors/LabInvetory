from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse

from .models import Category, Material, Loan, LoanItem
from .forms import (
    CategoryForm, MaterialForm, LoanForm, LoanItemFormSet,
    ReturnLoanForm
)

@login_required
def dashboard(request):
    total_materials = Material.objects.count()
    total_categories = Category.objects.count()
    active_loans = Loan.objects.filter(status='active').count()
    late_loans = Loan.objects.filter(status='late').count()
    
    if not request.user.is_staff:
        user_active_loans = Loan.objects.filter(
            user=request.user, 
            status__in=['active', 'late']
        )
    else:
        user_active_loans = None
    
    context = {
        'total_materials': total_materials,
        'total_categories': total_categories,
        'active_loans': active_loans,
        'late_loans': late_loans,
        'user_active_loans': user_active_loans,
    }
    return render(request, 'inventory/dashboard.html', context)

@staff_member_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

@staff_member_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'inventory/category_form.html', {'form': form})

@staff_member_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/category_form.html', {'form': form})

@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('category_list')
    return render(request, 'inventory/category_confirm_delete.html', {'category': category})