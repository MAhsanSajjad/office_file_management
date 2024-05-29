from django.contrib import admin
from user_app.models import FolderData, Folder, FolderDataAccess, FriendList, FriendRequest
# Register your models here.
admin.site.register(FolderData)
admin.site.register(Folder)
admin.site.register(FolderDataAccess)
admin.site.register(FriendList)
admin.site.register(FriendRequest)