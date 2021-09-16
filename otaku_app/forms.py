from django import forms
from .models import Title, Category, Subcategory

NA_BIEZACO = 'Na bieżąco'
W_TRAKCIE = "W trakcie"
PORZUCONE = "Porzucone"
SKONCZONE = "Skończone"
PLANOWANE = "Planowane"
WSTRZYMANE = "Wstrzymane"

CHOICES = (
    (NA_BIEZACO, "Na bieżąco"),
    (W_TRAKCIE, "W trakcie"),
    (PORZUCONE, "Porzucone"),
    (SKONCZONE, "Skończone"),
    (PLANOWANE, "Planowane"),
    (WSTRZYMANE, "Wstrzymane"),
)

class TitleForm(forms.ModelForm):
    """Formularz tytułu."""
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Wprowadź tytuł",
        }), label='')
    status = forms.ChoiceField(
        choices=CHOICES)

    class Meta:
        model = Title
        fields = ['name', 'status']
        labels = {
            'status': 'Status'
        }

class CategoryForm(forms.ModelForm):
    """Formularz kategorii."""
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Wprowadź kategorię",
        }), label='')
    status = forms.ChoiceField(
        choices=CHOICES)

    class Meta:
        model = Category
        fields = ['name', 'status']
        labels = {
            'name': 'Kategoria',
            'status': 'Status',
        }
        
class SubcategoryForm(forms.ModelForm):
    """Formularz podkategorii."""
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Wprowadź podkategorię",
        }), label='')
    status = forms.ChoiceField(
        choices=CHOICES)

    class Meta:
        model = Subcategory
        fields = ['name', 'status']
        labels = {
            'name': 'Podkategoria',
            'status': 'Status',
        }