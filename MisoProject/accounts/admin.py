from django.contrib import admin
from .models import Users, Item


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')  # 一覧表示で表示するフィールドを指定

admin.site.register(Users, UsersAdmin)  # Users モデルと UsersAdmin クラスを関連付けて登録
admin.site.register(Item)

# @admin.register(Items)
# class ItemsAdmin(admin.ModelAdmin):
#     list_display = ['user', 'name', 'used_miso', 'timestamp']
#     list_filter = ['used_miso']
#     search_fields = ['name']

# @admin.register(UsedMisoList)
# class UsedMisoListAdmin(admin.ModelAdmin):
#     list_display = ['item', 'timestamp']
#     search_fields = ['item__name']

# @admin.register(UsedMisoDetail)
# class UsedMisoDetailAdmin(admin.ModelAdmin):
#     list_display = ['item', 'thoughts', 'taste_rating', 'appearance_rating', 'timestamp']
#     search_fields = ['item__name']