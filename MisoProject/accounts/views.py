from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import Items, UsedMisoList
from .forms import UsedMisoListForm
from .models import UsedMisoDetail
from django.views import View
from .forms import UsedMisoDetailForm, ItemsForm




class HomeView(TemplateView):
    template_name = 'home.html'

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm


class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
@method_decorator(login_required, name='dispatch')    
class ItemsRegistView(View):
    template_name = 'item_regist.html'

    def get(self, request, *args, **kwargs):
        form = ItemsForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ItemsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('accounts:items_list')

        return render(request, self.template_name, {'form': form})
    

@method_decorator(login_required, name='dispatch')
class ItemsListView(View):
    template_name = 'items_list.html'

    def get(self, request, *args, **kwargs):
        items = Items.objects.filter(used_miso=False)
        return render(request, self.template_name, {'items': items})

    def post(self, request, *args, **kwargs):
        selected_items = request.POST.getlist('selected_items')
        for item_id in selected_items:
            item = Items.objects.get(id=item_id)
            item.used_miso = True
            item.save()
            UsedMisoList.objects.create(item=item)
        return redirect('accounts:items_list')


@method_decorator(login_required, name='dispatch')
class UsedMisoListView(View):
    template_name = 'used_miso_list.html'

    def get(self, request, *args, **kwargs):
        used_miso_list = UsedMisoList.objects.filter(item__user=request.user)
        print(used_miso_list)  # コンソールに出力
        return render(request, self.template_name, {'used_miso_list': used_miso_list})
    

class UsedMisoDetailView(View):
    template_name = 'used_miso_detail.html'

    def get(self, request, *args, **kwargs):
        form = UsedMisoDetailForm(prefix='used_miso_detail_form')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        used_miso_detail_form = UsedMisoDetailForm(request.POST, prefix='used_miso_detail_form')

        if used_miso_detail_form.is_valid():
            used_miso_detail_data = used_miso_detail_form.cleaned_data
            
            # Item フォームから item_id 取得
            item_id = used_miso_detail_form.cleaned_data['item']

            try:
                # ここで Item インスタンスを取得
               used_miso_detail_data['item'] = Items.objects.get(pk=item_id)
            except Items.DoesNotExist:
                # Item インスタンスが存在しない場合の処理
                error_message = '指定された Item インスタンスが存在しません。'
                return render(request, self.template_name, {'used_miso_detail_form': used_miso_detail_form, 'error_message': error_message})

            # Item インスタンスを保存
            used_miso_detail_data['item'].save() 

            # UsedMisoDetail モデルに保存
            UsedMisoDetail.objects.create(user=request.user, **used_miso_detail_data)

            return redirect('used_miso_list')  # 保存後に一覧ページなどにリダイレクト

        return render(request, self.template_name, {'used_miso_detail_form': used_miso_detail_form})


# @method_decorator(login_required, name='dispatch')
# class UsedMisoDetailView(View):
#     template_name = 'used_miso_detail.html'

#     def get(self, request, *args, **kwargs):
#         form = UsedMisoDetailForm(prefix='used_miso_detail_form')
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         used_miso_detail_form = UsedMisoDetailForm(request.POST, prefix='used_miso_detail_form')

#         if used_miso_detail_form.is_valid():
#             used_miso_detail_data = used_miso_detail_form.cleaned_data
            
#             # Item フォームから item_id 取得
#             item = used_miso_detail_form.cleaned_data['item']
            
#             # UsedMisoDetail モデルに保存
#             UsedMisoDetail.objects.create(user=request.user, item=item, **used_miso_detail_data)

#             return redirect('used_miso_list')  # 保存後に一覧ページなどにリダイレクト

#         return render(request, self.template_name, {'used_miso_detail_form': used_miso_detail_form})



# @method_decorator(login_required, name='dispatch')
# class UsedMisoDetailView(View):
#     template_name = 'used_miso_detail.html'

#     def get(self, request, *args, **kwargs):
#         form = UsedMisoDetailForm(prefix='used_miso_detail_form')
#         items_form = ItemsForm(prefix='items_form')
#         return render(request, self.template_name, {'form': form, 'items_form': items_form})

#     def post(self, request, *args, **kwargs):
#         used_miso_detail_form = UsedMisoDetailForm(request.POST, prefix='used_miso_detail_form')
#         items_form = ItemsForm(request.POST, prefix='items_form')

#         if used_miso_detail_form.is_valid() and items_form.is_valid():
#             used_miso_detail_data = used_miso_detail_form.cleaned_data
#             items_data = items_form.cleaned_data

#             # Items モデルに保存（既存のインスタンスを再利用）
#             item = get_object_or_404(Items, id=items_data['id'], user=request.user)

#             # UsedMisoDetail モデルに保存
#             used_miso_detail_data['item'] = item
#             UsedMisoDetail.objects.create(**used_miso_detail_data)

#             return redirect('used_miso_list')  # 保存後に一覧ページなどにリダイレクト

#         return render(request, self.template_name, {'used_miso_detail_form': used_miso_detail_form, 'items_form': items_form})


#元のコード
# @method_decorator(login_required, name='dispatch')
# class UsedMisoDetailView(View):
#     template_name = 'used_miso_detail.html'

#     def get(self, request, *args, **kwargs):
#         form = UsedMisoDetailForm(prefix='used_miso_detail_form')
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         used_miso_detail_form = UsedMisoDetailForm(request.POST, prefix='used_miso_detail_form')
#         items_form = ItemsForm(request.POST, prefix='items_form')

#         if used_miso_detail_form.is_valid() and items_form.is_valid():
#             used_miso_detail_data = used_miso_detail_form.cleaned_data
#             items_data = items_form.cleaned_data

#             # Items モデルに保存
#             item = Items.objects.create(**items_data)

#             # UsedMisoDetail モデルに保存
#             used_miso_detail_data['item'] = item
#             UsedMisoDetail.objects.create(**used_miso_detail_data)

#         return render(request, self.template_name, {'used_miso_detail_form': used_miso_detail_form, 'items_form': items_form})