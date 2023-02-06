from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(task)
admin.site.register(company_master)
admin.site.register(User_details)
admin.site.register(user_active_account)
admin.site.register(Role_master)
admin.site.register(Role_mapping)
admin.site.register(user_permission_mapping)
admin.site.register(space_master)
admin.site.register(space_access_permission_user)
admin.site.register(status_name_master)
admin.site.register(Create_meeting)
admin.site.register(RoomMember)
admin.site.register(sub_space_master)
admin.site.register(sub_space_access_permission)
admin.site.register(sub_space_checklist)
admin.site.register(tags_name_master)

admin.site.register(Add_task_master)
admin.site.register(Add_task_access_user)
admin.site.register(Add_task_checklist)
admin.site.register(Add_task_attachment)
admin.site.register(Add_task_comments)
admin.site.register(space_view_access_user)
admin.site.register(User_chat_room)
admin.site.register(userMessage)
admin.site.register(Notification)
admin.site.register(Task_time_details)
admin.site.register(History_task_time)
