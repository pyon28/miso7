from django.urls import path
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserView, ItemsDetailView, ItemsUpdateView, ItemsDeleteView,
     ItemsListView, UsedMisoListView, RegistUserCompleteView, item_regist_view) 
    #  ItemsRegistView,
app_name = 'accounts'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/', UserView.as_view(), name='user'),
    # path('item_regist/', ItemsRegistView.as_view(), name='item_regist'),
    path('item_regist/', item_regist_view, name='item_regist'),
    path('items_list/', ItemsListView.as_view(), name='items_list'),
    path('items_detail/<int:pk>/', ItemsDetailView.as_view(), name='items_detail'),
    path('used_miso_list/', UsedMisoListView.as_view(), name='used_miso_list'),
    path('items_update/<int:pk>/', ItemsUpdateView.as_view(), name='items_update'),
    path('dutems_delete/<int:pk>/', ItemsDeleteView.as_view(), name='items_delete'),
    path('regist_user_complete/', RegistUserCompleteView.as_view(), name='regist_user_complete'), 
   
    ] 


   
