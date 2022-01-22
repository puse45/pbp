from django import forms
from django.forms import DateInput


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'exclude' arg up to the superclass
        excluded = kwargs.pop("exclude_fields", [])
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        for field in excluded:
            self.fields.pop(field, None)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control ms"
            self.fields[field].widget.attrs["class"] = "form-control ms"
            if type(self.fields[field].widget) == forms.DateInput:
                self.fields[field].widget = DateInput(
                    attrs={"class": "form-control", "type": "date"}
                )
