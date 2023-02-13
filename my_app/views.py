from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from rest_framework.decorators import api_view
from itertools import chain
from .serializers import status_name_master_Serailzer

from rest_framework.response import Response
from datetime import datetime


from django.views.generic.base import TemplateView

class signup(TemplateView):

    def post(self,request,*args,**kwargs):
        companyname = self.request.POST.get("companyname")
        Username = self.request.POST.get("Username")
        email = self.request.POST.get("email")
        Phone = self.request.POST.get("Phone")
        password = self.request.POST.get("password")
        Photo = None
        try:
            Photo = self.request.FILES['Photo']
        except:
            pass
        if User.objects.filter(username=Username).exists():
                messages.warning(request,str("An account with the given username already exists"))
                return redirect(request.META['HTTP_REFERER'])
        else:
            if company_master.objects.filter(company_name = companyname).exists():
                company_model_data =company_master.objects.get(company_name = companyname)
                company_master_id = company_model_data.id
            else:
                company_save = company_master.objects.create(company_name =companyname,status="False")
                company_master_id = company_save.id
            user = User.objects.create_user(Username, password = password)
            user.save()
            user_data = User_details.objects.create(
                    company_id_id = company_master_id,
                    company_name =companyname,
                    auth_user = user,
                    photo = Photo,
                    username = Username,
                    email = email,
                    phone = Phone,
                    user_type = 'company_admin',
                    user_level = 'Manager',
                    status = "True"
                    )
            messages.success(request,"Successfully added User details")
            return redirect('user_login')
            pass

    template_name = 'signup.html'


def index(request):
    user_details_data = ""
    try:
        user_details_data = User_details.objects.get(auth_user=request.user)
    except:
        pass
    context = {
        "user_details_data":user_details_data
    }
    return render(request,'index.html',context)


def calendar(request):
    return render(request, 'calendar.html')


def chat(request):
    user_details_data = User_details.objects.get(auth_user=request.user)
    context = {
        "user_details_data":user_details_data
    }
    return render(request, 'chat.html',context)


def user_login(request):
    return render(request, 'user_login.html')

def meeting(request):
    meeting_data =""

    try:
        user_details_data = User_details.objects.get(auth_user=request.user)
        data = User_details.objects.get(auth_user=request.user)
        meeting_data = Add_meeting.objects.filter(invite_user_id__id=data.id).order_by('-id')
        status_name = status_name_master.objects.filter(company_id=userdetails_data.company_id)

    except:
        pass
    user_details_data = User_details.objects.get(auth_user=request.user)
    context = {
        "user_details_data":user_details_data,
        'meeting_data':meeting_data,
    }
    return render(request, 'meeting.html',context)



def create_new_meeting(request):
    if request.method == "POST":
        Title = request.POST.get("Title")
        meeting_dt = request.POST.get("meeting_dt")
        meeting_tm = request.POST.get("meeting_tm")
        invite_user_id = request.POST.getlist("invite_user_id")
        channel_name = request.POST.get("channel_name")
        Description = request.POST.get("Description")
        invite_user_model_data = User_details.objects.filter(id__in=invite_user_id)
        invite_user_list = list(invite_user_model_data.values_list('id',flat=True))
        data_save = Add_meeting.objects.create(Title=Title,meeting_dt=meeting_dt,meeting_tm=meeting_tm,channel_name=channel_name,Description=Description,completed_status="pending",created_by=request.user)
        for i in invite_user_list:
            data_save.invite_user_id.add(i)

        messages.success(request,"Scheduled a meeting")
        return redirect('meeting_management')

    



def new_company(request):
    company_data = company_master.objects.all()
    return render(request, 'new_company.html',{'company_data':company_data})

def new_meeting(request):
    return render(request, 'new_meeting.html')



def new_role(request):
    user_details_data = User_details.objects.get(auth_user=request.user)

    context={
        "user_details_data":user_details_data
    }
    return render(request, 'new_role.html',context)

def new_status(request):
    user_details_data = User_details.objects.get(auth_user=request.user)

    context={
        "user_details_data":user_details_data,

    }
    return render(request, 'new_status.html',context)

def new_user(request):
    company_data = company_master.objects.all()
    return render(request, 'new_user.html',{"company_data":company_data})



def base(request):
    return render(request, 'base.html')



from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
def login_action(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            user_data = ""
            try:
                user_data = User_details.objects.get(auth_user=user)
            except:
                pass
        
            st = user.is_superuser
            if user is not None:
                if st == True:
                    login(request, user)
                    return redirect('index')
                elif user_data:
                    login(request, user)
                    return redirect('index')
        except:
            messages.error(request, str("Incorrect username or password"))
            return redirect(request.META['HTTP_REFERER'])





# -----------------------------------------------------company_management-----------------------------------------------------------------


def company_management(request):

    user_data = User.objects.all().first()
    member_data = User_details.objects.all().exclude(created_by = user_data)
   
    data = company_master.objects.all()
    context = {
        "data" : data,
        "member_data" : member_data
    }
    return render(request, 'company_management.html',context)



from PIL import Image
import os
import PIL
import glob
import cv2

def company_add_action(request):
    if request.method == "POST":
        companyname = request.POST.get("companyname",False)
        logo =  request.FILES['logo']
        fixed_height = 400
        image = Image.open(logo)
        print("image.size",image.size)
        width_size = int(fixed_height/image.height * image.width)
        print("width_size:::::",width_size)
        resized_image = image.resize((width_size,fixed_height))
        print("resizeeeeeed:",resized_image.size)
        from django.conf import settings
        resized_image.save("media/company_logo/"+logo.name,quality=100)
        image_new1 = 'company_logo/'+logo.name
        
        tax_no = request.POST.get("tax_no",False)
        mobile_no = request.POST.get("mobile_no",False)
        website = request.POST.get("website",False)
        phone = request.POST.get("phone",False)
        email = request.POST.get("email",False)
        address = request.POST.get("address",False)

        if company_master.objects.filter(company_name=companyname).exists():
            messages.error(request,"Company name already exists")
            return redirect(request.META['HTTP_REFERER'])
        else:
            company_master.objects.create(
                company_name =companyname,
                company_logo = image_new1,
                tax_number = tax_no,
                mobile = mobile_no,
                website = website,
                phone = phone,
                email = email,
                address = address,
                created_by = request.user,
                status = "True"
                )
            messages.success(request,"Successfully added company details")
            return redirect('company_management')







# -----------------------------------------------------user_management-----------------------------------------------------------------

def user_management(request):
    user_data = User.objects.all().first()
    member_data = User_details.objects.all().exclude(created_by = user_data)
    
    data = User_details.objects.all()
    context = {
        "data" : data,
        "member_data":member_data
    }
    return render(request, 'user_management.html',context)


@api_view(['POST'])
def user_management_action(request):
    data = request.data
    photo =  request.FILES['photo']
    fixed_height = 128
    image = Image.open(photo)
    print("image.size",image.size)
    width_size = int(fixed_height/image.height * image.width)

    resized_image = image.resize((width_size,fixed_height))
    print("resizeeeeeed:",resized_image.size)
    from django.conf import settings
    resized_image.save("media/user_image/"+photo.name)
    image_new1 = 'user_image/'+photo.name
    if data['password_option'] == "Automatic":
        import string    
        import random
        S = 10
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
    else:
        password = request.POST.get("password",False)
    company_master_id = ''
    if User_details.objects.filter(username=data['username']).exists():
        messages.warning(request,"Username already exists")
        return redirect(request.META['HTTP_REFERER'])

    else:

        # super_admin add company admin(navabsir)

        if data['user_type'] == "company_admin":
            if company_master.objects.filter(company_name = data['companyname']).exists():
                company_model_data =company_master.objects.get(company_name = data['companyname'])
                company_master_id = company_model_data.id
            else:
                company_save = company_master.objects.create(company_name =data['companyname'],created_by = request.user,status="False")
                company_master_id = company_save.id
            user = User.objects.create_user(data['username'], password = password)
            user.save()
            user_data = User_details.objects.create(
                    company_id_id = company_master_id,
                    company_name =data['companyname'],
                    auth_user = user,
                    photo = image_new1,
                    name = data['name'],
                    username = data['username'],
                    password_option = data['password_option'],
                    password = password,
                    email = data['email'],
                    phone = data['phone'],
                    user_type = 'company_admin',
                    user_level = 'Manager',
                    created_by = request.user,
                    status = "True"
                    )
            messages.success(request,"Successfully added User details")
            return redirect('user_management')
            
        else:

            role_id = request.POST.getlist("role_id[]")
            
            role_description = request.POST.getlist("role_description[]")
            role_start_dt = request.POST.getlist("role_start_dt[]")
            role_end_dt = request.POST.getlist("role_end_dt[]")
            role_length = len(role_id)
            login_user_data = User_details.objects.get(auth_user=request.user)

            # company admin(navab sir) add company user senior(amar sir)
            user_id = data['manager_id']
           
            user_detail = User_details.objects.get(id=user_id)
            if login_user_data.user_type == "company_admin":
                
                user = User.objects.create_user(data['username'], password = password)
                user.save()
                user_data = User_details.objects.create(
                    company_id_id = login_user_data.company_id.id,
                    company_name =login_user_data.company_id.company_name,
                    auth_user = user,
                    photo = image_new1,
                    name = data['name'],
                    username = data['username'],
                    password_option = data['password_option'],
                    password = password,
                    email = data['email'],
                    phone = data['phone'],
                    user_type = 'company_user',
                    user_level = data['user_level'],
                    manager_auth_id = user_detail.auth_user.id, 
                    created_by = request.user,
                    status = "True"
                )

                data_save_active = user_active_account(user_id_id =user_data.id, active_user_id_id=login_user_data.id,active_auth_user_id_id=request.user.id)
                data_save_active.save()
                for i in range(0,role_length):
                    role_end_dt1 = role_end_dt[i]
                    if role_end_dt1 == "":
                        role_end_dt1 = None
                    data_save_user_role = user_permission_mapping(
                        auth_user_id = user,
                        user_id_id = user_data.id,
                        role_mapping_id_id = int(role_id[i]),
                        start_dt = role_start_dt[i],
                        end_dt = role_end_dt1,
                        description = role_description[i]
                    )
                    data_save_user_role.save()
                messages.success(request,"Successfully added new member")
                return redirect('member_management')

            # company user senior(amar) add company user junior(Amritha)

            elif login_user_data.user_type == "company_user":
                user = User.objects.create_user(data['username'], password = password)
                user.save()
                user_data = User_details.objects.create(
                    company_id_id = login_user_data.company_id.id,
                    company_name =login_user_data.company_id.company_name,
                    auth_user = user,
                    photo = image_new1,
                    name = data['name'],
                    username = data['username'],
                    password_option = data['password_option'],
                    password = password,
                    email = data['email'],
                    phone = data['phone'],
                    user_type = 'company_user',
                    user_level = data['user_level'],
                    manager_auth_id = user_detail.auth_user.id, 
                    created_by = request.user,
                    status = "True"
                    )
                login_user_active_account = user_active_account.objects.get(user_id_id=login_user_data.id)
                data_save_active = user_active_account(user_id_id =user_data.id,active_user_id_id=login_user_active_account.active_user_id.id,active_auth_user_id_id=login_user_active_account.active_auth_user_id.id)
                data_save_active.save()
                for i in range(0,role_length):

                    role_end_dt1 = role_end_dt[i]
                    if role_end_dt1 == "":
                        role_end_dt1 = None
                    data_save_user_role = user_permission_mapping(
                        auth_user_id_id = user.id,
                        user_id_id = user_data.id,
                        role_mapping_id_id = role_id[i],
                        start_dt = role_start_dt[i],
                        end_dt = role_end_dt1,
                        description = role_description[i]
                    )
                    data_save_user_role.save()
                messages.success(request,"Successfully added new member")
                return redirect('member_management')



# -----------------------------------------------------member_management-----------------------------------------------------------------

def member_management(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    manager_data = ""
    role_data = ""
    try:
        user_details_data = User_details.objects.get(auth_user=request.user)
        role_data = Role_master.objects.filter(company_id = user_details_data.company_id.id)
        manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )
        print("manager_data:::::",manager_data)
    except:
        pass


    user_permission_modal = user_permission_mapping.objects.filter(auth_user_id=request.user)
    user_permission_modal1 = list(user_permission_modal.values_list('role_mapping_id',flat=True))
    user_manage_all_permission = Role_mapping.objects.filter(role_master_id__in=user_permission_modal1,navbar_name="Team member",manage_all=True)

    user_details_data = User_details.objects.get(auth_user=request.user)
    if user_manage_all_permission:
        active_user_id = user_active_account.objects.get(user_id_id=user_details_data.id)
        user_active_account1 = user_active_account.objects.filter(active_auth_user_id_id =active_user_id.active_auth_user_id )
        child_user_id = list(user_active_account1.values_list('user_id__auth_user',flat=True))
        child_user_id.append(int(active_user_id.active_auth_user_id.id))
        member_data = User_details.objects.filter(created_by__in=child_user_id).exclude(auth_user = request.user)
    else:
        if user_details_data.user_type == "company_admin":
            user_active_account1 = user_active_account.objects.filter(active_auth_user_id =request.user)
            child_user_id = list(user_active_account1.values_list('user_id__auth_user',flat=True))
            child_user_id.append(int(request.user.id))
            member_data = User_details.objects.filter(created_by__in=child_user_id) 
            member_data1 = User_details.objects.filter(auth_user=request.user) 
            member_data = list(chain(member_data1,member_data))

        else:
            member_data = User_details.objects.filter(manager_auth=request.user)


    context = {
        "member_data" : member_data,
        "role_data":role_data,
        "user_details_data":user_details_data,
        "manager_data":manager_data,
        "today_date":today_date,
    }
    return render(request, 'member_management.html',context)


def new_member(request):
    manager_data = ""
    role_data = ""
    try:
        user_details_data = User_details.objects.get(auth_user=request.user)
        role_data = Role_master.objects.filter(company_id = user_details_data.company_id.id)
        manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )
    except:
        pass
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    context = {
        "manager_data":manager_data,
        "role_data":role_data,
        "today_date":today_date,
        "user_details_data":user_details_data
    }
    
    return render(request, 'new_member.html',context)


# -----------------------------------------------------role_management-----------------------------------------------------------------
def role_management(request):
    
    userdetails_data = User_details.objects.get(auth_user = request.user)

    role_data = Role_master.objects.filter(company_id = userdetails_data.company_id.id)

    context = {
        "role_data":role_data,
        "user_details_data":userdetails_data,
    }
    return render(request,"role_management.html",context)


def role_management_action(request):
    if request.method == "POST":
        user_data = User_details.objects.get(auth_user = request.user)
        data_save_role = Role_master.objects.create(
                role_name = request.POST.get('name'),
                description = request.POST.get('description'),
                status = "True",
                auth_user_id = request.user.id,
                created_by = request.user,
                company_id_id = user_data.company_id.id
            )

        Role_mapping.objects.create(
                role_master_id_id = data_save_role.id,
                navbar_name = "Company",
                read = request.POST.get('company_read',False),
                write = request.POST.get('company_write',False),
                edit = request.POST.get('company_edit',False),
                delete = request.POST.get('company_delete',False),
                view_all = request.POST.get('company_view_all',False),
                manage_all = request.POST.get('company_manage_all',False),
                created_by = request.user,
                status = "True"
            )

        Role_mapping.objects.create(
                role_master_id_id = data_save_role.id,
                navbar_name = "User",
                read =  request.POST.get('user_read',False),
                write =  request.POST.get('user_write',False),
                edit =  request.POST.get('user_edit',False),
                delete =  request.POST.get('user_delete',False),
                view_all =  request.POST.get('user_view_all',False),
                manage_all =  request.POST.get('user_manage_all',False),
                created_by = request.user,
                status = "True"
            )

        Role_mapping.objects.create(
                role_master_id_id = data_save_role.id,
                navbar_name = "Role",
                read = request.POST.get('role_read',False),
                write = request.POST.get('role_write',False),
                edit = request.POST.get('role_edit',False),
                delete = request.POST.get('role_delete',False),
                view_all = request.POST.get('role_view_all',False),
                manage_all = request.POST.get('role_manage_all',False),
                created_by = request.user,
                status = "True"
            )

        Role_mapping.objects.create(
                role_master_id_id = data_save_role.id,
                navbar_name = "Team member",
                read = request.POST.get('team_member_read',False),
                write = request.POST.get('team_member_write',False),
                edit = request.POST.get('team_member_edit',False),
                delete = request.POST.get('team_member_delete',False),
                view_all = request.POST.get('team_member_view_all',False),
                manage_all = request.POST.get('team_member_manage_all',False),
                created_by = request.user,
                status = "True"
            )


        Role_mapping.objects.create(
                role_master_id_id = data_save_role.id,
                navbar_name = "Tags",
                read = request.POST.get('tag_read',False),
                write = request.POST.get('tag_write',False),
                edit = request.POST.get('tag_edit',False),
                delete = request.POST.get('tag_delete',False),
                view_all = request.POST.get('tag_view_all',False),
                manage_all = request.POST.get('tag_manage_all',False),
                created_by = request.user,
                status = "True"
            )

        Role_mapping.objects.create(
                role_master_id_id = data_save_role.id,
                navbar_name = "Status",
                read = request.POST.get('status_read',False),
                write = request.POST.get('status_write',False),
                edit = request.POST.get('status_edit',False),
                delete = request.POST.get('status_delete',False),
                view_all = request.POST.get('status_view_all',False),
                manage_all = request.POST.get('status_manage_all',False),
                created_by = request.user,
                status = "True"
            )

    messages.success(request,"Successfully added Role")
    return redirect('role_management')


# -----------------------------------------------------task_status_management-----------------------------------------------------------------

def task_status_management(request):
    
    user_details_data = User_details.objects.get(auth_user=request.user)
    status_name = status_name_master.objects.filter(company_id=user_details_data.company_id)    

    context = {
        
        "status_name":status_name,
        "user_details_data":user_details_data
    }
    return render(request, 'task_status_management.html',context)


@api_view(['POST'])
def task_status_action(request):
    data = request.data
    user_data = User_details.objects.get(auth_user = request.user)
    print("data['status_color']:",data['status_color'])
    status_name_master.objects.create(active_user_id_id =user_data.id,
    active_auth_user_id_id =request.user.id ,status_name = data['status_name'],created_by = request.user,status="True",
    status_color=data['status_color'],company_id_id = user_data.company_id.id )
    messages.success(request,"Successfully added Status")
    return redirect('task_status_management')


# ----------------------------------------------------project_management-------------------------------------------------------------

def project_management(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    user_permission_modal = user_permission_mapping.objects.filter(auth_user_id=request.user)
    user_permission_modal1 = list(user_permission_modal.values_list('role_mapping_id',flat=True))
    user_manage_all_permission = Role_mapping.objects.filter(role_master_id__in=user_permission_modal1,navbar_name="Team member",manage_all=True)

    user_details_data = User_details.objects.get(auth_user=request.user)
    manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )
    if user_manage_all_permission:
        active_user_id = user_active_account.objects.get(user_id_id=user_details_data.id)
        user_active_account1 = user_active_account.objects.filter(active_auth_user_id_id =active_user_id.active_auth_user_id )
        child_user_id = list(user_active_account1.values_list('user_id__auth_user',flat=True))
        child_user_id.append(int(active_user_id.active_auth_user_id.id))
        member_data = User_details.objects.filter(created_by__in=child_user_id)
    else:
        if user_details_data.user_type == "company_admin":
            user_active_account1 = user_active_account.objects.filter(active_auth_user_id =request.user)
            child_user_id = list(user_active_account1.values_list('user_id__auth_user',flat=True))
            child_user_id.append(int(request.user.id))
            member_data = User_details.objects.filter(created_by__in=child_user_id).exclude(user_level = "Manager")
        else:
            member_data = User_details.objects.filter(manager_auth=request.user)

    role_data = Role_master.objects.filter(company_id = user_details_data.company_id.id)
    status_name = status_name_master.objects.filter(company_id=user_details_data.company_id)

    space_master_data = ""
    sub_space_data =""
    space_dept = ""
    space_member_data =""
    try:
        userdetails_data = User_details.objects.get(auth_user=request.user)

        # if user is company_admin (navab sir (all space of him))
        if userdetails_data.user_type == "company_admin":
            space_master_data = space_master.objects.filter(added_user_id=request.user)
            space_list = list(space_master_data.values_list('id',flat=True))
            print("space_list.first:",space_list[0])
            space_dept = space_master.objects.get(id=space_list[0])
            space_member_data = space_view_access_user.objects.filter(space_id=space_list[0])
            sub_space_data = sub_space_master.objects.filter(space_id =space_list[0])
        else:
            # if user is company_user(their space only)
            space_access_data = space_view_access_user.objects.filter(space_view_auth_id=request.user)
            user_permission_space = list(space_access_data.values_list('space_id',flat=True))
            space_master_data = space_master.objects.filter(id__in=user_permission_space)


            space_list = list(space_master_data.values_list('id',flat=True))
            sub_space_data = sub_space_master.objects.filter(space_id__in =space_list)

    except:
        pass

    if userdetails_data.user_type == "company_admin":
        space_data = space_master.objects.filter(added_user_id = request.user)

    context = {
    "member_data" : member_data,
    "role_data":role_data,
    "user_details_data":user_details_data,
    "status_name":status_name,
    "manager_data":manager_data,
    "space_master_data":space_master_data,
    "sub_space_data":sub_space_data,
    "space_dept":space_dept,
    "space_member_data":space_member_data,
    "today_date":today_date
    }
    return render(request, 'project_management.html',context)


# -----------------------------------------------------space_management-----------------------------------------------------------------

def space_add_action(request):
    if request.method == "POST":
        spacename = request.POST.get("spacename",False)
        task_status_add = request.POST.getlist("task_status_add",False)
        # if not task_status_add
        new_task_status_add = list(filter(None, task_status_add))
        print("new_task_status_add::::",new_task_status_add)
        if new_task_status_add:
            
            for t in new_task_status_add:
                user_data = User_details.objects.get(auth_user = request.user)
                status_name_master.objects.create(active_user_id_id =user_data.id,
                active_auth_user_id_id =request.user.id ,status_name = t,created_by = request.user,status="True",
                company_id_id = user_data.company_id.id )

        user_id_list = request.POST.getlist("manager_id")
        
        member_data = request.POST.getlist("member_data",False)
        list_new = user_id_list + member_data
        res = [*set(list_new)]
        print("res:::::::::::::",res)

        task_status_id = request.POST.getlist("task_status_name")
        task_status_data = status_name_master.objects.filter(id__in=task_status_id)
        task_status_list = list(task_status_data.values_list('id',flat=True))

        task_new_status_id = request.POST.getlist("task_status_add")
        task_new_status_data =status_name_master.objects.filter(status_name__in=task_new_status_id)
        task_new_status_list = list(task_new_status_data.values_list('id',flat=True))
        print("task_new_status_list:",task_new_status_list)

        status_list = task_status_list + task_new_status_list
        new_status = [*set(status_list)]
        print("new_status::::",new_status)

        user_data = User_details.objects.get(auth_user = request.user)
        if user_data.user_type == "company_admin":
            space_master_data = space_master.objects.create(space_name=spacename,
            added_user_id = request.user,
            status = "True",
            created_by = request.user
            )
            for j in user_id_list:
                user_details = User_details.objects.get(id=j)
                auth_data = user_details.auth_user
                space_master_data.manager_auth.add(auth_data)
            for k in new_status:
                space_master_data.task_status.add(k)

        else:
            user_active = user_active_account.objects.get(user_id=user_data.id)
            print("user_active:::::;",user_active)

            space_master_data = space_master.objects.create(space_name=spacename,
            active_account_id_id=user_active.active_user_id.id,
            added_user_id = request.user,
            status = "True",
            created_by = request.user
            )
            for j in user_id_list:
                user_details = User_details.objects.get(id=j)
                auth_data = user_details.auth_user
                space_master_data.manager_auth.add(auth_data)

            for k in new_status:
                space_master_data.task_status.add(k)
       

        for r in res:
            user_details = User_details.objects.get(id=r)
            auth_data = user_details.auth_user
            space_view_access_user.objects.create(space_id_id = space_master_data.id ,space_view_auth_id_id = auth_data.id,space_view_user_details_id =r)
        messages.success(request,"Successfully added Group")
        return redirect('project_management')

def get_bucket_details(request):
    space_id = request.GET.get("space_id")
    space_data = space_master.objects.get(id=space_id)
    return render(request,'get_bucket_details.html',{"bucket_data":space_data.task_status.all()})


def project_add_action(request):
    if request.method == "POST":
        space_id = request.POST.get("space_id")
        foldername = request.POST.get("foldername")
        member_data = request.POST.getlist("member_data",False)
        
        notes = request.POST.get("notes",False)
        bucket = request.POST.get("bucket",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        planning_start_date = request.POST.get("planning_start_date",False)
        planning_end_date = request.POST.get("planning_end_date",False)
        actual_start_date = request.POST.get("actual_start_date",False)
        actual_end_date = request.POST.get("actual_end_date",False)
        comments = request.POST.get("comments",False)
        checklist_item = request.POST.getlist("checklist",False)
        new_checklist_item = list(filter(None, checklist_item))
        print("new_checklist_item::::",new_checklist_item)
        
        user_data = User_details.objects.get(auth_user = request.user)
        if user_data.user_type == "company_admin":
            data_save = sub_space_master.objects.create(space_id_id = space_id,
            sub_space_name = foldername,
            bucket_mapping_id_id = bucket,
            progress = progress,
            priority = priority,
            notes = notes,
            Planning_start_date = planning_start_date,
            Planning_end_date = planning_end_date,
            Actual_start_date = actual_start_date,
            Actual_end_date = actual_end_date,
            added_user_id = request.user,
            created_by = request.user,status="True")

            for i in member_data:
                user_details = User_details.objects.get(id=i)
                data_save.invite_user_auth_id.add(user_details.auth_user.id)
                data_save.invite_user_details_id.add(i)

            for i in new_checklist_item:
                sub_space_checklist.objects.create(sub_space_id_id=data_save.id,
                milestone = i)

            try:
                # file_name = request.POST.get("file_name",False)
                attached_file =  request.FILES.getlist('attached_file')
                print("attached_file:",attached_file)
                for i in attached_file:

                    import os
                    filename = os.path.splitext(str(i))[0]
                    print("nameeeee",filename)
                    extension = os.path.splitext(str(i))[1]
                    print("extension:",extension)
                    sub_space_attachment.objects.create(sub_space_id_id=data_save.id,
                    file_name = filename,file_type =extension ,attached_file = i,added_by = request.user)

            except:
                pass
                

            user_data = User_details.objects.get(auth_user=request.user)
            if comments == "":
                print("nulll")
            else:

                sub_space_comments.objects.create(sub_space_id_id=data_save.id,
                added_by_id = user_data.id,user_auth_id_id =request.user.id ,comments = comments)

        else:
            user_active = user_active_account.objects.get(user_id=user_data.id)

            data_save = sub_space_master.objects.create(space_id_id = space_id,
            sub_space_name = foldername,
            bucket_mapping_id_id = bucket,
            progress = progress,
            priority = priority,
            notes = notes,
            Planning_start_date = planning_start_date,
            Planning_end_date = planning_end_date,
            Actual_start_date = actual_start_date,
            Actual_end_date = actual_end_date,
            active_account_id_id = user_active.active_user_id.id,
            added_user_id = request.user,
            created_by = request.user,status="True")

            for i in member_data:
                user_details = User_details.objects.get(id=i)
                data_save.invite_user_auth_id.add(user_details.auth_user.id)
                data_save.invite_user_details_id.add(i)

            for i in new_checklist_item:
                sub_space_checklist.objects.create(sub_space_id_id=data_save.id,
                milestone = i)


            try:
                # file_name = request.POST.get("file_name",False)
                attached_file =  request.FILES.getlist('attached_file')
                print("attached_file:",attached_file)
                for i in attached_file:
                    import os
                    filename = os.path.splitext(str(i))[0]
                    print("nameeeee",filename)
                    extension = os.path.splitext(str(i))[1]
                    print("extension:",extension)
                    sub_space_attachment.objects.create(sub_space_id_id=data_save.id,
                    file_name = filename,file_type =extension ,attached_file = i,added_by = request.user)

            except:
                pass

            user_data = User_details.objects.get(auth_user=request.user)
            if comments == "":
                print("nulll")
            else:
                sub_space_comments.objects.create(sub_space_id_id=data_save.id,
                added_by_id = user_data.id,user_auth_id_id =request.user.id ,comments = comments)

        for sp in member_data:
            user_details = User_details.objects.get(id=sp)
            sub_space_access_permission.objects.create(space_id_id = space_id ,sub_space_id_id=data_save.id,invite_user_details_id_id = sp,invite_user_auth_id_id = user_details.auth_user.id)
        messages.success(request,"Successfully added Project")
        return redirect(request.META['HTTP_REFERER'])


def update_project_details(request):
    if request.method == "POST":
        sub_space_id = request.POST.get("sub_space_id",False)
        project_name = request.POST.get("project_name",False)
        print("project_name:::::",project_name)
        tag_name = request.POST.getlist("tag_name",False)
        print("tag_name::",tag_name)
        tag_name.pop(0)
        
        print("tag_name:::::",tag_name)

        status_name = request.POST.get("status_name",False)
        print("status_name:::::",status_name)
        progress = request.POST.get("progress",False)
        print("progress:::::",progress)
        priority = request.POST.get("priority",False)
        print("priority:::::",priority)
        planning_start_date = request.POST.get("planning_start_date",False)
        print("planning_start_date:::::",planning_start_date)
        planning_end_date = request.POST.get("planning_end_date",False)
        print("planning_end_date:::::",planning_end_date)
        actual_start_date = request.POST.get("actual_start_date",False)
        print("actual_start_date:::::",actual_start_date)
        actual_end_date = request.POST.get("actual_end_date",False)
        print("actual_end_date:::::",actual_end_date)
        notes = request.POST.get("notes",False)
        print("notes:::::",notes)
        checklist_new = request.POST.getlist("checklist_new",False)
        print("checklist_new:::::",checklist_new)
       
        
        sub_space_master.objects.filter(id=sub_space_id).update(sub_space_name = project_name,bucket_mapping_id =status_name,progress=progress,priority=priority,Planning_start_date=planning_start_date,Planning_end_date=planning_end_date,
        Actual_start_date = actual_start_date,Actual_end_date = actual_end_date,notes = notes)

        today_date = datetime.today().strftime('%Y-%m-%d')

        try:
            for k in checklist_new:
                sub_space_checklist.objects.create(sub_space_id_id=sub_space_id,milestone=k,updated_by = request.user,updated_dt=today_date)
        except:
            pass
               

        sub_space = sub_space_master.objects.get(id=sub_space_id)
        for t in tag_name:
            sub_space.tag_id.add(t)

        messages.success(request,"Successfully updated Project details")
        return redirect(request.META['HTTP_REFERER'])






def view_group(request):
    space_id = request.GET.get("space_id")
    space_data = space_master.objects.get(id=space_id)
    today_date = datetime.today().strftime('%Y-%m-%d')

    space_member_data = space_view_access_user.objects.filter(space_id=space_id)

    user_details_data = User_details.objects.get(auth_user=request.user)
    
    sub_space_data = sub_space_master.objects.filter(space_id=space_id)

    context={
        "space_data":space_data,
        "today_date":today_date,
        "space_member_data":space_member_data,
        "sub_space_data":sub_space_data
    }
    return render(request, 'view_group.html',context)



def view_project_page(request):
    from.models import progress,priority
    from datetime import datetime
    today_date = datetime.today().strftime('%Y-%m-%d')

    sub_space_id = request.GET.get("sub_space_id")
    sub_space_data = sub_space_master.objects.get(id=sub_space_id)
    space_id = sub_space_data.space_id

    space_data = space_master.objects.get(id=space_id.id)

    sub_space_member_data = sub_space_master.objects.get(id=sub_space_id)

    task_data = Add_task_master.objects.filter(space_id = space_id,sub_space_id = sub_space_id,parent_id = None )

    user_details_data = User_details.objects.get(auth_user=request.user)
    dynamic_status = status_name_master.objects.filter(company_id=user_details_data.company_id)    
    tags_name = tags_name_master.objects.filter(company_id=user_details_data.company_id) 


    context = {
        "sub_space_member_data" : sub_space_member_data,
        "space_data":space_data,
        "sub_space_data":sub_space_data,
        "today_date":today_date,
        "bucket_data":space_data.task_status.all(),
        "progress":progress,
        "priority":priority,
        "today_date":today_date,
        "task_data":task_data,
        "sub_space_id":sub_space_id,
        "user_details_data":user_details_data,
        "dynamic_status":dynamic_status,
        "tags_name":tags_name,
    }
    return render(request, 'view_project_page.html',context)




def update_project(request):
    if request.method == "POST":
        sub_space_id = request.POST.get("sub_space_id",False)
        edit_project_name = request.POST.get("edit_project_name",False)
        edit_start_date = request.POST.get("edit_start_date",False)
        edit_end_date = request.POST.get("edit_end_date",False)
        edit_progress = request.POST.get("edit_progress",False)
        edit_priority = request.POST.get("edit_priority",False)
        edit_bucket = request.POST.get("edit_bucket",False)
        edit_checklist = request.POST.get("edit_checklist",False)

        sub_space_master.objects.filter(id=sub_space_id).update(sub_space_name = edit_project_name,bucket_mapping_id =edit_bucket,progress=edit_progress,priority=edit_priority,Planning_start_date=edit_start_date,Planning_end_date=edit_end_date)

        messages.success(request,"Successfully updated Project details")
        return redirect(request.META['HTTP_REFERER'])


def task_management_action(request):
    if request.method == "POST":
        member_checkbox = request.POST.getlist("member_checkbox")
        space_id = request.POST.get("space_id",False)
        sub_space_id = request.POST.get("sub_space_id",False)
        task_name = request.POST.get("task_name",False)
        notes = request.POST.get("notes",False)
        bucket = request.POST.get("bucket",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        start_date = request.POST.get("start_date",False)
        end_date = request.POST.get("end_date",False)
        checklist_item = request.POST.getlist("checklist",False)
        new_checklist_item = list(filter(None, checklist_item))
        print("new_checklist_item:",new_checklist_item)
        comments = request.POST.get("comments",False)

        task_master_save = Add_task_master.objects.create(space_id_id = space_id,
        sub_space_id_id = sub_space_id,
        task_name = task_name,
        bucket_mapping_id_id = bucket,
        progress = progress,
        priority = priority,
        notes = notes,
        start_date = start_date,
        end_date = end_date,
        task_status = "Main_task"
        )
        for i in member_checkbox:
            user_details = User_details.objects.get(id=i)
            task_access_user_save = Add_task_access_user.objects.create(add_task_id=task_master_save.id,
            invite_user_details_id_id =i,invite_user_auth_id_id=user_details.auth_user.id
            )

        for i in new_checklist_item:
            Add_task_checklist.objects.create(add_task_id_id=task_master_save.id,
            item_name = i)

        try:
            # file_name = request.POST.get("file_name",False)
            attached_file =  request.FILES.getlist('attached_file')
            print("attached_file:",attached_file)
            for i in attached_file:
                import os
                filename = os.path.splitext(str(i))[0]
                print("nameeeee",filename)
                extension = os.path.splitext(str(i))[1]
                print("extension:",extension)
                Add_task_attachment.objects.create(add_task_id_id=task_master_save.id,
                file_name = filename,file_type =extension ,attached_file = i,added_by = request.user)

        except:
            pass




        user_data = User_details.objects.get(auth_user=request.user)
        if comments == False:
            pass
        else:
            Add_task_comments.objects.create(add_task_id_id=task_master_save.id,
            added_by_id = user_data.id,user_auth_id_id =request.user.id ,comments = comments)

        messages.success(request,"Successfully added Task")
        return redirect(request.META['HTTP_REFERER'])


from django.db.models import Sum
from datetime import datetime, timedelta

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)





def view_task_page(request):
   
    from.models import progress,priority
    from datetime import datetime
    today_date = datetime.today().strftime('%Y-%m-%d')

    task_id = request.GET.get("task_id")
    print("task_id:",task_id)

    current_date = datetime.today().strftime('%Y-%m-%d')
    current_status = ""
    button_status = ""
    refresh_time_diff = ""
    try:
        task_time_data = Task_time_details.objects.get(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False")
        current_status = task_time_data.status 
        button_status = task_time_data.button_status

        format = '%H:%M:%S'
        starting_time = task_time_data.starting_time
        timer_start = str(starting_time.replace(microsecond=0))
        after_refresh_time = str(datetime.now().time().replace(microsecond=0)) 
        time_diff_delta1 = datetime.strptime(after_refresh_time, format) - datetime.strptime(timer_start, format)
        time_diff_datetime = datetime.strptime(str(time_diff_delta1), '%H:%M:%S')
        refresh_time_diff = time_diff_datetime.time()

        if button_status == "Resume":
            
            previous_counter_data = task_time_data.counter
            s9 = "00:00:00"
            time9 = datetime.strptime(str(refresh_time_diff), format) - datetime.strptime(s9, format)
            time8 = datetime.strptime(str(previous_counter_data), format) - datetime.strptime(s9, format)
            total_counter = time8 + time9
            time_counter1 = datetime.strptime(str(total_counter), '%H:%M:%S')
            refresh_time_diff = time_counter1.time()

        elif button_status == "Pause":
            refresh_time_diff = task_time_data.counter
        else:
            pass
    except:
        pass




    time_details = Task_time_details.objects.filter(task_id=task_id,user_auth_id = request.user)
    total_hr = ""
    try : 
        total_price = sum(time_details.values_list('total_second', flat=True))
        total_hr = convert(total_price)
    except:
        pass





    task_data = Add_task_master.objects.get(id=task_id)
    space_id = task_data.space_id
    sub_space_data = task_data.sub_space_id


    sub_task_data = Add_task_master.objects.filter(parent_id = task_id)
   

    space_data = space_master.objects.get(id=space_id.id)

    task_member_data = Add_task_access_user.objects.filter(add_task=task_id)

    # task_data = Add_task_master.objects.filter(space_id = space_id,sub_space_id = sub_space_id )

    user_details_data = User_details.objects.get(auth_user=request.user)
    dynamic_status = status_name_master.objects.filter(company_id=user_details_data.company_id)    
    tags_name = tags_name_master.objects.filter(company_id=user_details_data.company_id) 



    parent_id = task_id

    context = {
        "task_member_data" : task_member_data,
        "space_data":space_data,
        "sub_space_data":sub_space_data,
        "task_data":task_data,
        "today_date":today_date,
        "bucket_data":space_data.task_status.all(),
        "progress":progress,
        "priority":priority,
        "today_date":today_date,
        "sub_task_data":sub_task_data,
        'parent_id':parent_id,
        "dynamic_status":dynamic_status,
        "tags_name":tags_name,

        "current_status":current_status,
        "button_status":button_status,
        "refresh_time_diff":refresh_time_diff,
        "time_details":time_details,
        'total_hr':total_hr
    }
    return render(request, 'view_task_page.html',context)


from datetime import datetime
def start_timer_action(request):

    current_date = datetime.today().strftime('%Y-%m-%d')
    task_id = request.GET.get("task_id")
    status = request.GET.get("status")

    # ------------------------stopwatch start----------------------------------------------------------

    if status == "start":
        start_time =datetime.now() 
        c_user = request.user.id
        user_data = User_details.objects.get(auth_user = c_user)
        try:
            task_time_data = Task_time_details.objects.get(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False")
        except:
            Task_time_details.objects.create(starting_time=start_time,current_date=current_date,
            task_id_id = task_id,user_auth_id_id = c_user,user_details_id_id =user_data.id,status = "True",button_status="Start",end_status = "False")
        pass

    # ---------------------------------------stopwatch pause---------------------------------------

    elif status == "pause":
        pause_time = str(datetime.now().time().replace(microsecond=0))
        format = '%H:%M:%S'
        task_time_data = Task_time_details.objects.get(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False")
        starting_time = task_time_data.starting_time
        start_time = str(starting_time.replace(microsecond=0))
        time_diff_delta = datetime.strptime(pause_time, format) - datetime.strptime(start_time, format)

        time_diff1 = datetime.strptime(str(time_diff_delta), '%H:%M:%S')      
        time_diff = time_diff1.time()
        seconds = (time_diff.hour * 60 + time_diff.minute) * 60 + time_diff.second

        if task_time_data.counter == None:
            Task_time_details.objects.filter(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False").update(counter = time_diff,total_second=seconds, status ="True",button_status ="Pause")
        else:
            previous_counter_data = task_time_data.counter
            s9 = "00:00:00"
            time9 = datetime.strptime(str(time_diff), format) - datetime.strptime(s9, format)
            time8 = datetime.strptime(str(previous_counter_data), format) - datetime.strptime(s9, format)
            total_counter = time8 + time9
            time_counter1 = datetime.strptime(str(total_counter), '%H:%M:%S')
            time_count = time_counter1.time()
            seconds = (time_count.hour * 60 + time_count.minute) * 60 + time_count.second
            Task_time_details.objects.filter(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False").update(counter = time_count,total_second=seconds,status ="True",button_status ="Pause")
        History_task_time.objects.create(task_time_id_id =task_time_data.id,starting_time = start_time,end_time = pause_time,counter = time_diff,
        task_id_id = task_id,user_auth_id_id = request.user.id)

    # --------------------------------------------stopwatch resume-----------------------------------------------------

    elif status == "resume":
        task_time_data = Task_time_details.objects.filter(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False").update(starting_time =datetime.now(),status="True",button_status="Resume")

    # ------------------------------------------stopwatch stop---------------------------------------------------

    else:

        task_time_data = Task_time_details.objects.get(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False")
        status = task_time_data.status
        button_status = task_time_data.button_status

        # ----------------------------------------when user click start to stop---------------------------------------------

        if status == "True" and button_status == "Start" :
            
            stop_time = str(datetime.now().time().replace(microsecond=0))
            format = '%H:%M:%S'
            task_time_data = Task_time_details.objects.get(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False")
            starting_time = task_time_data.starting_time
            end_status = task_time_data.end_status
            start_time = str(starting_time.replace(microsecond=0))            
            time_diff_delta = datetime.strptime(stop_time, format) - datetime.strptime(start_time, format)
            time_diff1 = datetime.strptime(str(time_diff_delta), '%H:%M:%S')
            time_diff = time_diff1.time()
            seconds = (time_diff.hour * 60 + time_diff.minute) * 60 + time_diff.second
            Task_time_details.objects.filter(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False").update(counter = time_diff,total_second=seconds,status = False,button_status = "Stop",end_status = "True")
            History_task_time.objects.create(task_time_id_id =task_time_data.id,starting_time = start_time,end_time = stop_time,counter = time_diff,
            task_id_id = task_id,user_auth_id_id = request.user.id)

        # ------------------------------------------when user click start to pause to stop---------------------------------------------

        elif status == "True" and button_status == "Pause" :
            Task_time_details.objects.filter(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False").update(status = False,button_status = "Stop",end_status = "True")
            
        # ------------------------------------------when user click start to pause to resume to stop---------------------------------------------

        elif status == "True" and button_status == "Resume" :            
            stop_time = str(datetime.now().time().replace(microsecond=0))
            format = '%H:%M:%S'
            task_time_data = Task_time_details.objects.get(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False")
            starting_time = task_time_data.starting_time
            start_time = str(starting_time.replace(microsecond=0))            
            time_diff_delta = datetime.strptime(stop_time, format) - datetime.strptime(start_time, format)
           
            time_diff1 = datetime.strptime(str(time_diff_delta), '%H:%M:%S')
            time_diff = time_diff1.time()
            previous_counter_data = task_time_data.counter
            s9 = "00:00:00"
            time9 = datetime.strptime(str(time_diff), format) - datetime.strptime(s9, format)
            time8 = datetime.strptime(str(previous_counter_data), format) - datetime.strptime(s9, format)
            total_counter = time8 + time9
            time_counter1 = datetime.strptime(str(total_counter), '%H:%M:%S')
            time_count = time_counter1.time()
            seconds = (time_count.hour * 60 + time_count.minute) * 60 + time_count.second
            Task_time_details.objects.filter(current_date=current_date,user_auth_id=request.user,task_id=task_id,end_status = "False").update(counter = time_count,total_second=seconds,status ="False",button_status ="Stop",end_status = "True")
            History_task_time.objects.create(task_time_id_id =task_time_data.id,starting_time = start_time,end_time = stop_time,counter = time_diff,
            task_id_id = task_id,user_auth_id_id = request.user.id)

    return JsonResponse({"message":"success"})





def sub_task_action(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id") #child_id
        space_id = request.POST.get("space_id")
        sub_space_id = request.POST.get("sub_space_id") #parent_id

        member_checkbox = request.POST.getlist("member_checkbox")
        sub_task_name = request.POST.get("sub_task_name",False)
        notes = request.POST.get("notes",False)
        bucket = request.POST.get("bucket",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        start_date = request.POST.get("start_date",False)
        end_date = request.POST.get("end_date",False)        
        comments = request.POST.get("comments",False)


        task_master_save = Add_task_master.objects.create(space_id_id = space_id,sub_space_id_id = sub_space_id,parent_id_id = task_id,
        task_name =sub_task_name,
        bucket_mapping_id_id=bucket,
        progress = progress,
        priority = priority,
        notes = notes,
        start_date = start_date,
        end_date = end_date,
        task_status = "sub_task"
        )

        for i in member_checkbox:
            user_details = User_details.objects.get(id=i)
            task_access_user_save = Add_task_access_user.objects.create(add_task_id=task_master_save.id,
            invite_user_details_id_id =i,invite_user_auth_id_id=user_details.auth_user.id
            )

        messages.success(request,"Successfully added Sub Task")
        return redirect(request.META['HTTP_REFERER'])







def demo(request):

    sub_space_master_data = sub_space_master.objects.get(id=1)
    space_id = space_master.objects.get(id=1)

    task_data = Add_task_master.objects.filter(space_id = space_id.id,sub_space_id = sub_space_master_data.id)

    for i in task_data:

        sub_task_data = Sub_tasks.objects.filter(parent_id=i.id,dynamic_status = False)
        print("sub_task_data::::::",sub_task_data)

        
    return render(request,'demo.html',context)


# -----------------------------------------------------tags_management-----------------------------------------------------------------

def tags_management(request):
    
    user_details_data = User_details.objects.get(auth_user=request.user)
    tags_name = tags_name_master.objects.filter(company_id=user_details_data.company_id)    

    context = {
        
        "tags_name":tags_name,
        "user_details_data":user_details_data
    }
    return render(request, 'tags_management.html',context)


@api_view(['POST'])
def tags_add_action(request):
    data = request.data
    user_data = User_details.objects.get(auth_user = request.user)
    tags_name_master.objects.create(active_user_id_id =user_data.id,
    active_auth_user_id_id =request.user.id ,tags_name = data['tags_name'],created_by = request.user,status="True",
    tags_color=data['tags_color'],company_id_id = user_data.company_id.id )
    messages.success(request,"Successfully added Tags")
    return redirect('tags_management')


def new_tags(request):
    user_details_data = User_details.objects.get(auth_user=request.user)
    context={
        "user_details_data":user_details_data,
    }
    return render(request, 'new_tags.html',context)


def project_management_board(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    user_details_data = User_details.objects.get(auth_user=request.user)

    space_id =  request.GET.get("space_id")
    space_datas = space_master.objects.get(id=space_id)

    space_master_data = ""
    try:
        userdetails_data = User_details.objects.get(auth_user=request.user)

        # if user is company_admin (navab sir (all space of him))
        if userdetails_data.user_type == "company_admin":
            space_master_data = space_master.objects.get(id=space_id)
           
    
        else:
            # if user is company_user(their space only)
            space_access_data = space_view_access_user.objects.filter(space_view_auth_id=request.user)
            user_permission_space = list(space_access_data.values_list('space_id',flat=True))
            space_master_data = space_master.objects.filter(id__in=user_permission_space)

            space_list = list(space_master_data.values_list('id',flat=True))

    except:
        pass

    if user_details_data.user_type == "company_admin":
        space_data = space_master.objects.filter(added_user_id = request.user)
    
    
    try:

        space_model = space_master.objects.get(id=space_id)
        status_model_data =list(space_model.task_status.values_list('id',flat=True))
        queryset = status_name_master.objects.filter(id__in=status_model_data)
        data_model = status_name_master_Serailzer(queryset,many=True,context={'space_id':space_id}).data
        space_member_data = space_view_access_user.objects.filter(space_id=space_id)
        print("space_member_data11111111111111111:",space_member_data)


    except:
        pass
    
    context = {
    "user_details_data":user_details_data,
    "space_master_data":space_master_data,
    "today_date":today_date,
    "space_datas":space_datas,
    "bucket_data":space_datas.task_status.all(),
    "data_model":data_model,
    "space_member_data":space_member_data
    }
    return render(request, 'project_management_board.html',context)


def get_group_details(request):
    space_member_data =""
    today_date = datetime.today().strftime('%Y-%m-%d')
    space_id = request.GET.get("space_id")
    space_dept = space_master.objects.get(id=space_id)
    sub_space_data = sub_space_master.objects.filter(space_id=space_id)

    space_member_data = space_view_access_user.objects.filter(space_id=space_id)
    context = {
        "today_date":today_date,
        "sub_space_data":sub_space_data,
        "space_dept":space_dept,
        "space_member_data":space_member_data

    }
    return render(request,'get_group_details.html',context)



def project_tree_structure(request):
    sub_space_id = request.GET.get("project_id")
    sub_space_data = sub_space_master.objects.get(id=sub_space_id)
    task_details = Add_task_master.objects.filter(sub_space_id=sub_space_id,parent_id = None)
    space_id = sub_space_data.space_id_id
    data_space_model = space_master.objects.get(id=space_id)
    space_task_status = data_space_model.task_status.all()
    print("space_task_status:::::::::",str(space_task_status))
    
    context ={
        "task_details":task_details,
        "sub_space_data":sub_space_data,
        "sub_space_id":sub_space_id,
        'space_task_status':space_task_status
        
    }
    return render(request, "project_tree_structure.html",context)




def export_pdf(request):
    sub_space_id = request.GET.get("sub_space_id")
    sub_space_data = sub_space_master.objects.get(id=sub_space_id)
    task_details = Add_task_master.objects.filter(sub_space_id=sub_space_id,parent_id = None)
    space_id = sub_space_data.space_id_id
    data_space_model = space_master.objects.get(id=space_id)
    space_task_status = data_space_model.task_status.all()

    context ={
        "task_details":task_details,
        "sub_space_data":sub_space_data,
        "sub_space_id":sub_space_id,
        'space_task_status':space_task_status
    }
    return render(request, "export_pdf.html",context )


from django.http import JsonResponse
from django.forms.models import model_to_dict

import xlwt
from django.http import HttpResponse

def export_excel(request):
    sub_space_id=request.GET.get('sub_space_id')
    subspace_data = sub_space_master.objects.get(id=sub_space_id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="project_structure.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Project details',cell_overwrite_ok=True)  
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Name']
   
    
    for col_num in range(len(columns)):
        style = xlwt.easyxf('pattern: pattern solid, fore_colour black;'
                              'font: colour white, bold True;align: horiz center')
        ws.write_merge(0, 0, 0, 5, subspace_data.sub_space_name,style)
    
    # for col_num in range(len(columns)):
    #     print("heiiiiiii:::::::",str(columns[col_num]))
        
    #     ws.write(1, col_num, columns[col_num], font_style) 


    font_style = xlwt.XFStyle()
    

    final_tree = list()
    i1 = 0
    data_new_list = [{"name":"Name","i1":i1}]
    

    def get_tree12(task_details,i1):
        tree = model_to_dict(task_details, fields=['task_name', 'start_date', 'end_date'])
        if task_details.sub_task.all().exists():
            children = list()
            for child in task_details.sub_task.all():
                i1 = i1+1
                data_new_list.append({'name':child.task_name,"i1":i1})
                children.append(get_tree12(child,i1))
                i1 = i1-1
            tree['subs'] = children
            i1 = i1-1
        return tree


    for task_details in Add_task_master.objects.filter(parent_id__isnull=True,sub_space_id =sub_space_id):
        data_new_list.append({'name':task_details.task_name,"i1":i1})
        final_tree.append(get_tree12(task_details,i1))
        i1 = 0

    print("data_new_list:::::::",str(data_new_list))
    
        
    ws.col(0).width = 20000
    for row in data_new_list:

        row_num += 1
        count1 = row['i1']
        name = "    "*int(count1)+"→"+row['name']
        style = xlwt.easyxf('font: bold 1, color red;')
        if row['name'] == "Name":
            ws.write(row_num, col_num, row['name'], font_style) 
        else:

            ws.write(row_num, col_num, name, style)
        
    wb.save(response)
    return response


    # rows = intractive_map.objects.filter(id__in=sub_space_id).annotate(statusnew=Case(When(current_status='0',then=Value("Available")),When(current_status='1',then=Value("Price Quotation")),When(current_status='2',then=Value("Sold")),When(current_status='3',then=Value("Cancelled")))).values_list('Name', 'Phoneno', 'UnitNo', 'BlockNo','UnitArea','LandArea','UType','Price','statusnew')    
    
    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, row[col_num], font_style)



def update_project_status(request):
    project_id = request.GET.get("project_id")
    status_id = request.GET.get("status_id")
    data_update = sub_space_master.objects.filter(id=project_id).update(bucket_mapping_id_id=status_id)
    messages.success(request,str("Status updated"))
    return redirect(request.META['HTTP_REFERER'])


def update_task_status(request):
    task_id = request.GET.get("task_id")
    status_id = request.GET.get("status_id")
    data_update = Add_task_master.objects.filter(id=task_id).update(bucket_mapping_id_id=status_id)
    messages.success(request,str("Status updated"))
    return redirect(request.META['HTTP_REFERER'])




   

