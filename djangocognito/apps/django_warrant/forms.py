from django import forms


class RegisterationForm(forms.Form):
    first_name = forms.CharField(max_length=200,required=True)
    last_name = forms.CharField(max_length=200,required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=200,required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    

class ConfirmRegisterationForm(forms.Form):
    confirmation_code = forms.CharField(max_length=200,required=True)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=200,required=True)

class ConfirmForgotPasswordForm(forms.Form):
    confirmation_code = forms.CharField(max_length=200,required=True)
    new_password = forms.CharField(max_length=200,required=True)

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=200,required=True)
    last_name = forms.CharField(max_length=200,required=True)
    phone_number = forms.CharField(max_length=30,required=True)
    gender = forms.ChoiceField(choices=(('female','Female'),('male','Male')),required=True)
    address = forms.CharField(max_length=200,required=True)
    preferred_username = forms.CharField(max_length=200,required=True)
    api_key = forms.CharField(max_length=200, required=False)
    api_key_id = forms.CharField(max_length=200, required=False)

class APIKeySubscriptionForm(forms.Form):
    plan = forms.ChoiceField(required=True)

    def __init__(self, plans=[], users_plans=[], *args, **kwargs):
        self.base_fields['plan'].choices = [(p.get('id'),p.get('name')) for p in plans if not p.get('id') in users_plans]
        super(APIKeySubscriptionForm, self).__init__(*args, **kwargs)
