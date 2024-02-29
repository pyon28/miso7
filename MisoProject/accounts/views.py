from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from .forms import ItemForm
from django.views.generic import UpdateView, DetailView, CreateView, DeleteView, ListView
from .models import Item


class HomeView(TemplateView):
    template_name = 'home.html'

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:user_login')
   

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember', False)  # フィールドが存在しない場合はデフォルト値 False を使用する
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)




#元のコード
# class UserLoginView(LoginView):
#     template_name = 'user_login.html'
#     authentication_form = UserLoginForm

#     def form_valid(self, form):
#         remember = form.cleaned_data['remember']
#         if remember:
#             self.request.session.set_expiry(1200000)
#         return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class ItemsRegistView(CreateView):
    template_name = 'item_regist.html'
    form_class = ItemForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ログインしたユーザー情報をフォームに渡す
        return kwargs

    def get_success_url(self):
        return reverse_lazy('accounts:items_list')
    
 

    
class ItemsListView(ListView):
    template_name = 'items_list.html'
    model = Item
    
    def get_queryset(self):
        # ログインユーザーのみのアイテムリストを取得
        user_items = Item.objects.filter(user=self.request.user)
        return user_items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # ユーザーのアイテムリスト
        user_items = Item.objects.filter(user=user)

        # チェックされたアイテムリスト
        checked_items = user_items.filter(used_miso=True)

        # used_miso_list に表示するアイテムリスト
        context['used_miso_list'] = checked_items
        return context


    
class UsedMisoListView(ListView):
    template_name = 'used_miso_list.html'
    model = Item

    def get_queryset(self):
        user = self.request.user
        queryset = Item.objects.filter(user=user, used_miso=True)
        
        # ログ出力
        print("取得されるアイテム:", queryset)
        
        return queryset
    
    

class ItemsDetailView(DetailView):
   template_name = 'items_detail.html'
   model = Item
   
   
class ItemsDeleteView(DeleteView):
    template_name = 'items_delete.html'
    model = Item
    success_url = reverse_lazy('accounts:items_list')  
   
   

class ItemsUpdateView(UpdateView):
    template_name = 'items_update.html'
    model = Item
    fields = ('name', 'image', 'used_miso', 'thoughts', 'taste_rating', 'appearance_rating',)
    success_url = reverse_lazy('accounts:items_list')
 
    def form_valid(self, form):
        item = form.save(commit=False)
        if 'image' in self.request.FILES:
            item.image = self.request.FILES['image']
        item.save()
        return super().form_valid(form)
    
    
    

