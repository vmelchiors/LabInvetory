from django.contrib import admin
from .models import Category, Material, Loan, LoanItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'available_quantity', 'total_quantity', 'location']
    list_filter = ['category']
    search_fields = ['name', 'description']

class LoanItemInline(admin.TabularInline):
    model = LoanItem
    extra = 1

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'loan_date', 'expected_return_date', 'return_date', 'status']
    list_filter = ['status', 'loan_date']
    search_fields = ['user__username', 'user__email']
    inlines = [LoanItemInline]
    
    def save_model(self, request, obj, form, change):
        if obj.status == 'returned' and not obj.return_date:
            obj.return_date = timezone.now()
        super().save_model(request, obj, form, change)