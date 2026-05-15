from django import forms

from .models import User


class UserForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "bg-transparent border border-white/50 rounded-lg px-4 py-2.5 w-full text-white outline-none focus:border-white transition-colors",
            "placeholder": "Enter your username",
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "bg-transparent border border-white/50 rounded-lg px-4 py-2.5 w-full text-white outline-none focus:border-white transition-colors",
            "placeholder": "Enter your password",
        }),
    )


class UserAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Leave blank to keep the current password unchanged.",
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_password(self):
        pw = self.cleaned_data.get("password")
        if not pw and not self.instance.pk:
            raise forms.ValidationError("Password is required for new users.")
        return pw
