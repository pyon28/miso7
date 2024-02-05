from django.urls import path
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserView,
    ItemsRegistView, ItemsListView, UsedMisoListView, UsedMisoDetailView
)

app_name = 'accounts'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/', UserView.as_view(), name='user'),
    path('item_regist/', ItemsRegistView.as_view(), name='item_regist'),
    path('items_list/', ItemsListView.as_view(), name='items_list'),
    path('used_miso_list/', UsedMisoListView.as_view(), name='used_miso_list'),
    # path('used_miso_detail/', UsedMisoDetailView.as_view(), name='used_miso_detail'),
    path('used_miso_detail/<int:item_id>/', UsedMisoDetailView.as_view(), name='used_miso_detail'),
   
]