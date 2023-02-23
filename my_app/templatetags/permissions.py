from ast import arg
from os import name, stat
from django import template
import json
register = template.Library()
from django.contrib.auth.models import User
from my_app.models import *
from datetime import date

@register.filter(name='company_nav_perm_check')
def company_nav_perm_check(value,args):
    user_dat = User.objects.get(id=value)
    try:
        user_details = User_details.objects.get(auth_user=user_dat)
    except:
        pass
    
    st = user_dat.is_superuser
    if st == True:
        if args == "Role" or args == "Team member":
            return False
        else:
            return True
    if user_details.user_type == "company_admin":
        if args == "Role" or args == "Team member" or args == "Tags" or args == "Status":
            return True
    else:
        today = date.today()
        permission_status = False
        try:

            data_user_role = user_permission_mapping.objects.filter(auth_user_id=value,end_dt__gte=today,start_dt__lte=today) |  user_permission_mapping.objects.filter(auth_user_id=value,end_dt=None,start_dt__lte=today)
            role_id = list(data_user_role.values_list("role_mapping_id",flat=True))
            check_data = Role_mapping.objects.filter(role_master_id__in=role_id,navbar_name=args,read="True")
            if check_data:
                permission_status = True
            return permission_status
        except:
            return permission_status
        

from datetime import date
today = date.today()

@register.filter(name='due_date_check_sub_space')
def due_date_check_sub_space(value,args):
    due_date_data = sub_space_master.objects.filter(Planning_end_date__lt=today,progress="In progress") | sub_space_master.objects.filter(Planning_end_date__lt=today,progress="Not Started")
    for i in due_date_data :
        if i.id == args :
            return True
        else:
            pass


@register.filter(name='due_date_check_task')
def due_date_check_task(value,args):
    due_date_data = Add_task_master.objects.filter(end_date__lt=today,progress="In progress") | Add_task_master.objects.filter(end_date__lt=today,progress="Not Started")
    for i in due_date_data :
        if i.id == args :
            return True
        else:
            pass



@register.filter(name='due_date_project_checklist')
def due_date_project_checklist(value,args):
    due_date_data = sub_space_checklist.objects.filter(due_date__lt=today)
    for i in due_date_data :
        if i.id == args :
            return True
        else:
            pass



@register.filter(name='due_date_task_checklist')
def due_date_task_checklist(value,args):
    due_date_data = Add_task_checklist.objects.filter(due_date__lt=today)
    for i in due_date_data :
        if i.id == args :
            return True
        else:
            pass




@register.filter
def index_f(value, args):
    s1 = "/" in args
    s2 = " " in args
    if s1 == True:
        data = args.split("/")
   
        try:
            if data[0][0] == data[1][0]:

                result = data[0][0]+data[1][1]
            else:
                result = data[0][0]+data[1][1]
        except:
            result = data[0][0]
            pass
        pass
        return result

    
    elif s2 == True:
        data = args.split(" ")
        try:
            result = data[0][0]+data[1][0]
            
        except:
            result = data[0][0]
            pass
    
        return result

    else:
        result = args[0]+args[-1]
        return result








@register.inclusion_tag('tree_structure.html')
def tree_structure(task):
    subs = task.sub_task.all()
    return {"subs": subs}