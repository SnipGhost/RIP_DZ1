from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from GameManager.models import Game, Profile

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'autofocus': True, 'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class GameManagerRegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Пароль не совпал с подтверждением"
    }

    class Meta:
        model = Profile
        fields = ['username', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class GameCreationForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'game_image', 'platform']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        game = super().save(commit=False)
        if commit:
            game.save()
        game.owner.set([self.user])
        return game


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'avatar', 'description')

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user')
            super().__init__(*args, **kwargs)
            self.user = user
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'})

        def save(self, commit=True):
            profile = super().save(commit=False)
            if commit:
                profile.save()
            return profile


class GameCreateForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'game_image', 'platform']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        game = super().save(commit=False)
        if commit:
            game.save()
        game.owner.set([self.user])
        return game
