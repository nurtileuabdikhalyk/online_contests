from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Result, Participant, Contest


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'phone', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Есіміңіз'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 747 000 00 00'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Хабарлама', 'rows': 4})
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Есіміңіз"}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Тегіңіз"}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Құпия сөз"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Құпия сөзді қайталаңыз"}))

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+7 747 000 00 00"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'phone')


class LoginForm(forms.ModelForm):
    login = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Құпия сөз"}))

    class Meta:
        model = User
        fields = ('login', 'password',)


class ResultForm(forms.ModelForm):

    def __init__(self, user, contest, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['participant'] = forms.ModelChoiceField(
            queryset=Participant.objects.filter(user=self.user), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

        self.fields['contest'] = forms.ModelChoiceField(
            queryset=Contest.objects.filter(id=contest.id), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

    class Meta:
        model = Result
        fields = ('participant', 'contest', 'file')

