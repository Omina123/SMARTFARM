from django import forms
from .models import Field, Crop, CustomUser

class FieldCreationForm(forms.ModelForm):
    # We include fields for both models to create them at once
    crop_name = forms.CharField(max_length=100, label="Crop Name (e.g. Maize)")
    variety = forms.CharField(max_length=100)
    planting_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    expected_harvest_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    acreage = forms.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Field
        fields = ['name', 'agent', 'stage']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field Name (e.g. North Sector)'}),
            'agent': forms.Select(attrs={'class': 'form-select'}),
            'stage': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Requirement #2: Ensure only Field Agents can be assigned
        self.fields['agent'].queryset = CustomUser.objects.filter(user_type='2')
from django import forms
from .models import Field

class FieldUpdateForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['stage', 'notes']
        widgets = {
            'stage': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter current observations, pests seen, or weather impacts...'
            }),
        }