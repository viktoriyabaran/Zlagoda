from django import forms

from .models import User

CHECKBOX_CLASS = "w-4 h-4 accent-white cursor-pointer"


class LayoutForm(forms.Form):
    conditional_groups: dict[str, list[str]] = {}

    def iter_layout(self):
        nested = {c for children in self.conditional_groups.values() for c in children}
        for bound_field in self:
            if bound_field.name in nested:
                continue
            yield self._row(bound_field)

    def _row(self, bound_field):
        if bound_field.name in self.conditional_groups:
            return {
                "type": "toggle",
                "field": bound_field,
                "children": [
                    self._row(self[c])
                    for c in self.conditional_groups[bound_field.name]
                ],
            }
        return {"type": "field", "field": bound_field}


class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "bg-transparent border border-white/50 rounded-lg px-3 py-2 w-full text-white text-sm outline-none focus:border-white",
                "placeholder": "Enter your username",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "bg-transparent border border-white/50 rounded-lg px-3 py-2 w-full text-white text-sm outline-none focus:border-white",
                "placeholder": "Enter your password",
            }
        ),
    )


class UserAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Leave blank to keep the current password unchanged.",
    )

    class Meta:
        model = User
        fields = ["username", "password", "employee"]

    def clean_password(self):
        pw = self.cleaned_data.get("password")
        if not pw and not self.instance.pk:
            raise forms.ValidationError("Password is required for new users.")
        return pw
