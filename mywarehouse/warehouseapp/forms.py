from django import forms
from .models import Product

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
