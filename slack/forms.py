from django import forms

class IsitupForm(forms.Form):
    command = forms.CharField(max_length=500)
    text = forms.CharField(max_length=500)
    token = forms.CharField(max_length=500)

    def clean_token(self):
        data = self.cleaned_data['token']
        if "25FJ7Qx1iJRW4pgeaK5re5Mm" != data:
            raise forms.ValidationError("The token for the slash command doesn't match. Check your script.")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
