from django import forms


class OrderForm(forms.Form):
    customer_email = forms.EmailField(label="Email клиента", required=True)
    serial = forms.CharField(label="Серия робота", max_length=5, required=True)
