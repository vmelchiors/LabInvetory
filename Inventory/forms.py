from django import forms
from .models import Material, Loan, LoanItem, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'total_quantity', 'available_quantity', 'location', 'category']

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['user', 'expected_return_date', 'notes', 'loan_date']
        widgets = {
            'expected_return_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class LoanItemForm(forms.ModelForm):
    class Meta:
        model = LoanItem
        fields = ['material', 'quantity']

    def __init__(self, *args, **kwargs):
        super(LoanItemForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.filter(available_quantity__gt=0)

LoanItemFormSet = forms.inlineformset_factory(
    Loan, LoanItem, form=LoanItemForm, extra=1, can_delete=True
)

class ReturnLoanForm(forms.Form):
    returned_quantity = forms.IntegerField(min_value=1, label='Quantidade a Devolver')