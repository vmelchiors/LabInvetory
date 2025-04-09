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

@login_required
def material_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    materials = Material.objects.all()
    
    if query:
        materials = materials.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_id:
        materials = materials.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'materials': materials,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'inventory/material_list.html', context)

@login_required
def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'inventory/material_detail.html', {'material': material})

@staff_member_required
def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.available_quantity = material.total_quantity
            material.save()
            messages.success(request, 'Material criado com sucesso!')
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'inventory/material_form.html', {'form': form})

@staff_member_required
def material_update(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material atualizado com sucesso!')
            return redirect('material_list')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'inventory/material_form.html', {'form': form})

@staff_member_required
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material excluído com sucesso!')
        return redirect('material_list')
    return render(request, 'inventory/material_confirm_delete.html', {'material': material})

@login_required
def loan_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    if request.user.is_staff:
        loans = Loan.objects.all().order_by('-loan_date')
    else:
        loans = Loan.objects.filter(user=request.user).order_by('-loan_date')

    if query:
        loans = loans.filter(
            Q(user__username__icontains=query) |
            Q(materials__name__icontains=query)
        ).distinct()
    
    if status:
        loans = loans.filter(status=status)
    
    if start_date:
        loans = loans.filter(loan_date__gte=start_date)
    
    if end_date:
        loans = loans.filter(loan_date__lte=end_date)
    
    context = {
        'loans': loans,
        'query': query,
        'status': status,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'inventory/loan_list.html', context)

@login_required
def my_loans(request):

    loans = Loan.objects.filter(user=request.user).order_by('-loan_date')
    return render(request, 'inventory/my_loans.html', {'loans': loans})

@login_required
def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if not request.user.is_staff and loan.user != request.user:
        messages.error(request, 'Você não tem permissão para acessar este empréstimo.')
        return redirect('dashboard')
    return render(request, 'inventory/loan_detail.html', {'loan': loan})

@login_required
def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        formset = LoanItemFormSet(request.POST)

        if form.is_valid():
            loan = form.save(commit=False)

            if not request.user.is_staff:
                loan.user = request.user
            loan.save()

            formset = LoanItemFormSet(request.POST, instance=loan)

            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        loan_item = form.save(commit=False)
                        material = loan_item.material
                        quantity = loan_item.quantity

                        if material.available_quantity >= quantity:
                            material.available_quantity -= quantity
                            material.save()
                        else:
                            loan.delete()
                            messages.error(request, f'Quantidade insuficiente de {material.name}. Disponível: {material.available_quantity}')
                            return redirect('loan_create')

                formset.save()
                messages.success(request, 'Empréstimo registrado com sucesso!')
                return redirect('loan_detail', pk=loan.pk)

    else:
        initial_data = {}
        if not request.user.is_staff:
            initial_data = {'user': request.user}

        form = LoanForm(initial=initial_data)
        if not request.user.is_staff:
            form.fields['user'].widget.attrs['readonly'] = True

        formset = LoanItemFormSet()

    return render(request, 'inventory/loan_form.html', {
        'form': form,
        'formset': formset,
    })


@login_required
def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)

    if not request.user.is_staff and loan.user != request.user:
        messages.error(request, 'Você não tem permissão para realizar esta devolução.')
        return redirect('dashboard')

    if loan.status == 'returned':
        messages.info(request, 'Este empréstimo já foi completamente devolvido.')
        return redirect('loan_detail', pk=loan.pk)
    
    if request.method == 'POST':
        for loan_item in loan.loanitem_set.all():
            material = loan_item.material
            remaining = loan_item.quantity - loan_item.returned_quantity
            
            if remaining > 0:
                loan_item.returned_quantity = loan_item.quantity
                loan_item.save()
                
                material.available_quantity += remaining
                material.save()
        
        loan.status = 'returned'
        loan.return_date = timezone.now()
        loan.save()
        
        messages.success(request, 'Todos os itens foram devolvidos com sucesso!')
        return redirect('loan_detail', pk=loan.pk)
    
    return render(request, 'inventory/loan_return_confirm.html', {'loan': loan})

@login_required
def loan_item_return(request, pk):
    loan_item = get_object_or_404(LoanItem, pk=pk)
    loan = loan_item.loan

    if not request.user.is_staff and loan.user != request.user:
        messages.error(request, 'Você não tem permissão para realizar esta devolução.')
        return redirect('dashboard')

    if loan_item.returned_quantity >= loan_item.quantity:
        messages.info(request, 'Este item já foi completamente devolvido.')
        return redirect('loan_detail', pk=loan.pk)
    
    if request.method == 'POST':
        form = ReturnLoanForm(request.POST)
        if form.is_valid():
            return_qty = form.cleaned_data['returned_quantity']
            remaining = loan_item.quantity - loan_item.returned_quantity
            
            if return_qty <= remaining:
                loan_item.returned_quantity += return_qty
                loan_item.save()
                
                material = loan_item.material
                material.available_quantity += return_qty
                material.save()

                all_returned = all(
                    item.returned_quantity >= item.quantity 
                    for item in loan.loanitem_set.all()
                )
                
                if all_returned:
                    loan.status = 'returned'
                    loan.return_date = timezone.now()
                    loan.save()
                
                messages.success(request, f'{return_qty} unidades de {material.name} devolvidas com sucesso!')
            else:
                messages.error(request, f'Quantidade inválida. Restante a devolver: {remaining}')
            
            return redirect('loan_detail', pk=loan.pk)
    else:
        form = ReturnLoanForm()
    
    remaining = loan_item.quantity - loan_item.returned_quantity
    context = {
        'form': form,
        'loan_item': loan_item,
        'loan': loan,
        'remaining': remaining,
    }
    
    return render(request, 'inventory/loan_item_return.html', context)