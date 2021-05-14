from django import forms


class RegForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )
    email = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        )
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Логин',
                'id': 'cin',
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'id': 'cin',
            }
        )
    )


class CreateVoteForm(forms.Form):
    votename = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Название',
            }
        )
    )
    about = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Подробнее',
            }
        )
    )
    variant = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'variant',
                'placeholder': 'Вариант ответа',
            }
        )
    )


class ComplainForm(forms.Form):

    textarea = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'main-area',
            }
        )
    )
