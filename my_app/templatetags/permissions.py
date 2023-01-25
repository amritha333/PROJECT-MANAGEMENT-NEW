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
        if args == "Role" or args == "Team member":
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
    due_date_data = sub_space_master.objects.filter(end_date__lt=today,progress="inprogress") | sub_space_master.objects.filter(end_date__lt=today,progress="not_started")
    for i in due_date_data :
        if i.id == args :
            return True
        else:
            pass


@register.filter(name='due_date_check_task')
def due_date_check_task(value,args):
    due_date_data = Add_task_master.objects.filter(end_date__lt=today,progress="inprogress") | Add_task_master.objects.filter(end_date__lt=today,progress="not_started")
    for i in due_date_data :
        if i.id == args :
            return True
        else:
            pass
