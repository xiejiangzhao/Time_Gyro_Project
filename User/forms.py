from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
     
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    birthday = forms.DateField(label = 'birthday', widget=forms.DateTimeInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(
        choices=((True,'male'),(False,'female'),),
        widget = forms.RadioSelect
    )
    class Meta:
        model = User
        fields = ['username','nick_name']

    # 验证两次输入
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)  # 继承父类的save方法 并重写
        user.set_password(self.cleaned_data["password1"])
        user.birthday = self.cleaned_data["birthday"]
        user.gender = self.cleaned_data["gender"]

        if commit:
            user.save()   # 保存创建的密码
        return user


class UserForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',widget=forms.PasswordInput())
