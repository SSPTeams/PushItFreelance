from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    telegram_id = forms.CharField(max_length=255, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    is_employer = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("is_employer"):
            if not cleaned_data.get("description"):
                self.add_error("description", "This field is required for employers")
        return cleaned_data