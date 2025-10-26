from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating categories.
    """
    class Meta:
        model = Category
        fields = ['name', 'category_type', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Ex: Salário, Alimentação'
            }),
            'category_type': forms.Select(attrs={
                'class': 'form-select w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-12 p-1 bg-slate-700 border border-slate-600 rounded-lg cursor-pointer'
            }),
        }
        labels = {
            'name': 'Nome da Categoria',
            'category_type': 'Tipo de Categoria',
            'color': 'Cor'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_type'].choices = [
            ('', 'Selecione um tipo'),
            (Category.CategoryType.INCOME, 'Entrada'),
            (Category.CategoryType.EXPENSE, 'Saída')
        ]
