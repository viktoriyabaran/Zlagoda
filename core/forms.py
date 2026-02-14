from django import forms


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
