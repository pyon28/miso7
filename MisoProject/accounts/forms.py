from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from .models import Item
from django.forms import ClearableFileInput

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='ユーザー名')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None:
            return None
    
        if len(password) < 8:
             raise forms.ValidationError('パスワードは8文字以上で入力してください。')
        return password

        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user



class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
   

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['user', 'name', 'image', 'used_miso', 'thoughts', 'taste_rating', 'appearance_rating',]
        widgets = {
            'image': ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control-file'}),  # ClearableFileInput を使用
            'user': forms.HiddenInput(),  # user フィールドを非表示にする
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        if user:
             # ユーザーが指定されている場合は、フォーム内の user フィールドにそのユーザーをセット
            self.fields['user'].initial = user.id  # ユーザーIDを初期値として設定する
            self.fields['user'].widget = forms.HiddenInput()  # user フィールドを非表示にする
        
         # used_miso フィールドにチェックボックスを追加
        self.fields['used_miso'].widget = forms.CheckboxInput()



        
        







