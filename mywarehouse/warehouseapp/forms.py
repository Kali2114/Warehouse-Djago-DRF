from django import forms
from .models import Product, Company

class BaseProductForms(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.title().strip()

class ReceiveProductForm(BaseProductForms):
    class Meta(BaseProductForms.Meta):
       pass

class IssueProductForm(BaseProductForms):
    class Meta(BaseProductForms.Meta):
        fields = ['name', 'quantity']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name').strip().title()

        if Company.objects.filter(name=name).exists():
            raise forms.ValidationError('Company with this name already exists.')

        return name

class CompanyDeleteForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name'].strip().title()

        if not Company.objects.filter(name=name).exists():
            raise forms.ValidationError('The provided company does not exist.')

        return name