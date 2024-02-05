from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from .models import Items
from .models import UsedMisoList, UsedMisoDetail

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='ユーザー名')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


# class UserLoginForm(forms.Form):
#     email = forms.EmailField(label='メールアドレス')
#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態を保持する', required=False)


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        # fields = ['name', 'image','user']
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ItemsForm, self).__init__(*args, **kwargs)
        if user:
             # ユーザーが指定されている場合は、フォーム内の user フィールドにそのユーザーをセット
            self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()  # user フィールドを非表示にする
        
        
    def ItemsForm_as_p(self):
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True,
        )    


class UsedMisoListForm(forms.ModelForm):
    class Meta:
        model = UsedMisoList
        fields = ['item']
        
        

class UsedMisoDetailForm(forms.ModelForm):
    class Meta:
        model = UsedMisoDetail
        fields = ['thoughts', 'taste_rating', 'appearance_rating', 'item']

    def __init__(self, *args, **kwargs):
        super(UsedMisoDetailForm, self).__init__(*args, **kwargs)

        # Item フォームの表示を変更
        self.fields['item'].widget = forms.HiddenInput()

    def clean_item(self):
        item_id = self.cleaned_data['item']
        try:
            item = Items.objects.get(pk=item_id)
        except Items.DoesNotExist:
            raise forms.ValidationError('指定されたアイテムが存在しません。')
        return item

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user']
        if commit:
            instance.save()
        return instance






#元のコード
# class UsedMisoDetailForm(forms.ModelForm):
#     class Meta:
#         model = UsedMisoDetail
#         fields = ['thoughts', 'taste_rating', 'appearance_rating','item']
        
#     def __init__(self, *args, **kwargs):
#         super(UsedMisoDetailForm, self).__init__(*args, **kwargs)
        
#         # ItemsForm のフィールドを追加
#         self.fields['item_form'] = ItemsForm(prefix='items_form', instance=self.instance.item)
        
#     def clean_item(self):
#         # ItemsForm のクリーンデータを取得
#         item_form_data = self.cleaned_data.get('item_form')
#         # ItemsForm から Items インスタンスを保存
#         item = item_form_data.save(commit=False)
#         item.user =  self.instance.user  # UsedMisoDetail のユーザー情報を設定
#         item.save()
#         return item    