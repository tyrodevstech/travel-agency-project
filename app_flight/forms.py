from django import forms
from .models import OrderFlight

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