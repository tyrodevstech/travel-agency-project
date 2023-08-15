from django import forms
from app_tour.models import TourOrderModel, TourPaymentsModel

class TourPackageOrderForm(forms.ModelForm):

    class Meta:
        model = TourOrderModel
        fields = ['journey_date', 'adult_traveler', 'child_traveler', 'infant_traveler']

        widgets = {
            'journey_date': forms.TextInput(attrs={'class': 'py-4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full !pl-10 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500', 'placeholder': 'Select Journey Date', 'type': 'date', 'required': 'required'}),
            'adult_traveler': forms.NumberInput(attrs={'class': 'py-4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Adult', 'min': '0', 'required': 'required'}),
            'child_traveler': forms.NumberInput(attrs={'class': 'mt-2 py-4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Children', 'min': '0'}),
            'infant_traveler': forms.NumberInput(attrs={'class': 'mt-2 py-4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Infant', 'min': '0'}),
        }



class TourPaymentsForm(forms.ModelForm):

    class Meta:
        model = TourPaymentsModel
        fields = ['user_card_name', 'user_card_number', 'user_cvc_number', 'user_postal_code']

        widgets = {
            'user_card_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'Name', 'required': 'required'}),
            'user_card_number': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'xxxx-xxxx-xxxx-xxxx', 'min': '0', 'required': 'required'}),
            'user_cvc_number': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': '***', 'min': '0'}),
            'user_postal_code': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'e.g. 12345', 'min': '0'}),
        }