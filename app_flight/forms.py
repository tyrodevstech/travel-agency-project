from django import forms
from .models import OrderFlight, Payment

class OrderFlightForm(forms.ModelForm):
    class Meta:
        model = OrderFlight
        fields = [
            "title",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "nationality",
        ]

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop("category", None)
        super().__init__(*args, **kwargs)
        if self.category == "adult":
            self.fields["title"].choices = [
                ("MR.", "MR."),
                ("MRS.", "MRS."),
                ("MS.", "MS."),
            ]
        elif self.category == "child":
            self.fields["title"].choices = [
                ("MASTER.", "MASTER."),
                ("MISS.", "MISS."),
            ]
        elif self.category == "infant":
            self.fields["title"].choices = [
                ("INFANT.", "INFANT."),
            ]


class FlightPaymentsForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['user_card_name', 'user_card_number', 'user_cvc_number', 'user_postal_code']

        widgets = {
            'user_card_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Name', 'required': 'required'}),
            'user_card_number': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'xxxx-xxxx-xxxx-xxxx', 'min': '0', 'required': 'required'}),
            'user_cvc_number': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': '***', 'min': '0'}),
            'user_postal_code': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'e.g. 12345', 'min': '0'}),
        }