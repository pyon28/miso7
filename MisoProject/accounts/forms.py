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

# name = forms.CharField(label='商品名', )
    # image = forms.ImageField(label='画像')  
    # used_miso = forms.BooleanField(label='使った味噌')
    # thoughts = forms.CharField(label='メモ・感想', widget=forms.Textarea)
    # taste_rating = forms.IntegerField(label='味')
    # appearance_rating = forms.IntegerField(label='見た目')
   

# class ItemForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['user', 'name', 'image', 'used_miso', 'thoughts', 'taste_rating', 'appearance_rating',]
#         widgets = {
#             'image': forms.FileInput(attrs={'accept': 'image/*',}), 
#             'user': forms.HiddenInput(),  # user フィールドを非表示にする
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(ItemForm, self).__init__(*args, **kwargs)
#         if user:
#              # ユーザーが指定されている場合は、フォーム内の user フィールドにそのユーザーをセット
#             self.fields['user'].initial = user.id  # ユーザーIDを初期値として設定する
#             self.fields['user'].widget = forms.HiddenInput()  # user フィールドを非表示にする
        
        
#          # used_miso フィールドにチェックボックスを追加
#         self.fields['used_miso'].widget = forms.CheckboxInput()


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'image', 'used_miso', 'thoughts', 'taste_rating', 'appearance_rating']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}), 
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # ユーザーを直接渡す
            self.fields['user'].widget = forms.HiddenInput()

    
         #used_miso フィールドにチェックボックスを追加
        self.fields['used_miso'].widget = forms.CheckboxInput()


        
        







