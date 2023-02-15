from django.contrib import admin
from django import views
from django.urls import path,include

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.user_login,name=''),
    path('index',views.index,name='index'),
    path('calendar',views.calendar,name='calendar'),
    path('chat',views.chat,name='chat'),
    path('company_management',views.company_management,name='company_management'),
    path('user_login',views.user_login,name='user_login'),
    path('meeting',views.meeting,name='meeting'),
    path('member_management',views.member_management,name='member_management'),
    path('new_company',views.new_company,name='new_company'),
    path('new_meeting',views.new_meeting,name='new_meeting'),
    path('new_member',views.new_member,name='new_member'),
    path('new_role',views.new_role,name='new_role'),
    path('new_status',views.new_status,name='new_status'),
    path('new_user',views.new_user,name='new_user'),
    path('project_management',views.project_management,name='project_management'),
    path('role_management',views.role_management,name='role_management'),
    path('task_status_management',views.task_status_management,name='task_status_management'),
    path('user_management',views.user_management,name='user_management'),
    path('view_group',views.view_group,name='view_group'),
    path('view_project_page',views.view_project_page,name='view_project_page'),
    path('base',views.base,name='base'),
    path('logout',auth_views.LogoutView.as_view(),name="logout"),

    path('login_action',views.login_action,name='login_action'),
    path('company_add_action',views.company_add_action,name='company_add_action'),
    path('user_management_action',views.user_management_action,name='user_management_action'),
    path('role_management_action',views.role_management_action,name='role_management_action'),
    path('task_status_action',views.task_status_action,name='task_status_action'),
    path('space_add_action',views.space_add_action,name='space_add_action'),
    path('get_bucket_details',views.get_bucket_details,name='get_bucket_details'),
    path('project_add_action',views.project_add_action,name='project_add_action'),
    path('task_management_action',views.task_management_action,name='task_management_action'),
    path('view_task_page',views.view_task_page,name='view_task_page'),
    path('sub_task_action',views.sub_task_action,name='sub_task_action'),
    path('update_project_details',views.update_project_details,name='update_project_details'),
    path('tags_management',views.tags_management,name='tags_management'),
    path('new_tags',views.new_tags,name='new_tags'),
    path('tags_add_action',views.tags_add_action,name='tags_add_action'),
    path('demo',views.demo,name='demo'),
    path('signup',views.signup.as_view(),name='signup'),
    path('project_management_board',views.project_management_board,name='project_management_board'),
    path('get_group_details',views.get_group_details,name='get_group_details'),

    path('start_timer_action',views.start_timer_action,name='start_timer_action'),

    path('project_tree_structure',views.project_tree_structure,name='project_tree_structure'),
    path('export_pdf',views.export_pdf,name='export_pdf'),
    
    path("export_excel/", views.export_excel, name="export_excel"),
    path('update_project_status',views.update_project_status,name='update_project_status'),

    path('update_task_status',views.update_task_status,name='update_task_status'),

    path('get_project_comment',views.get_project_comment,name='get_project_comment'),

    path('generate_client_access_link',views.generate_client_access_link,name='generate_client_access_link'),
    path('open_project/<str:name>',views.open_project,name='open_project'),




]