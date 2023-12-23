from django import forms

class ReceiveProductForm(forms.Form):
    product_name = forms.CharField()
    price = forms.FloatField()
    quantity = forms.IntegerField()

    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']
        return product_name.capitalize()

class IssueProductForm(forms.Form):
    product_name = forms.CharField()
    quantity = forms.IntegerField()

    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']
        return product_name.capitalize()