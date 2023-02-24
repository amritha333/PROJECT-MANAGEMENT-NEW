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
        name = self.request.POST.get("name")
        try:
            photo =  request.FILES['Photo']
            fixed_height = 128
            image = Image.open(photo)
            print("image.size",image.size)
            width_size = int(fixed_height/image.height * image.width)

            resized_image = image.resize((width_size,fixed_height))
            print("resizeeeeeed:",resized_image.size)
            from django.conf import settings
            resized_image.save("media/user_image/"+photo.name)
            image_new1 = 'user_image/'+photo.name
       
        except:
            pass
        if User.objects.filter(username=Username).exists():
                messages.warning(request,str("An account with the given username already exists"))
                return redirect(request.META['HTTP_REFERER'])
        else:
            if company_master.objects.filter(company_name = companyname).exists():
                data1 = company_master.objects.get(company_name = companyname)
                
                if User_details.objects.filter(company_id_id = data1.id,user_type = "company_admin"):
                    messages.warning(request,"Company admin already exist")
                    return redirect('user_management_new')
                else:

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
                    name = name,
                    auth_user = user,
                    photo = image_new1,
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
    company_data = company_master.objects.all()
    template_name = 'signup.html'

    


def index(request):
    user_details_data = ""
    member_data = ""
    try:

        user_details_data = User_details.objects.get(auth_user = request.user)
        member_data = User_details.objects.filter(company_id =user_details_data.company_id).exclude(auth_user=request.user)
    except:
        pass

    project_count = sub_space_master.objects.filter(created_by=request.user).count()

    task_count = Add_task_master.objects.filter(created_by=request.user).count()

    completed_count =  Add_task_master.objects.filter(created_by=request.user,progress = "Completed").count()

    progress_count =  Add_task_master.objects.filter(created_by=request.user,progress = "In progress").count()
   
    context = {
        "user_details_data":user_details_data,
        "member_data":member_data,
        "project_count":project_count,
        "task_count":task_count,
        "completed_count":completed_count,
        "progress_count":progress_count
    }
    return render(request,'index.html',context)


def calendar(request):
    return render(request, 'calendar.html')


def chat(request):
    member_data = ""
    user_details_data = User_details.objects.get(auth_user = request.user)
    member_data = User_details.objects.filter(company_id =user_details_data.company_id).exclude(auth_user=request.user)

    context = {
        "member_data":member_data
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
        status_name = status_name_master.objects.filter(company_id=user_details_data.company_id)

    except:
        pass
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


def company_management_new(request):
    user_data = User.objects.all().first()
    member_data = User_details.objects.all().exclude(created_by=user_data)

    data = company_master.objects.all()
    context = {
        "data": data,
        "member_data": member_data
    }
    return render(request, 'company_management_new.html', context)



def edit_company_modal(request):
    id = request.GET.get("id")
    data = company_master.objects.all()
    company = company_master.objects.get(id=id)
    context = {
        'data':data,
        'company':company
    }
    return render(request, 'edit_company_modal.html',context)




from PIL import Image
import os
import PIL
import glob
import cv2

def company_add_action(request):
    if request.method == "POST":
        companyname1 = request.POST.get("companyname",False)
        companyname = companyname1.title()
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
            return redirect('company_management_new')



def edit_company_action(request):
    if request.method == "POST":
        companyname1 = request.POST.get("companyname", False)
        companyname = companyname1.title()

        company_id = request.POST.get("company_id",False)
        tax_no = request.POST.get("tax_no", False)
        mobile_no = request.POST.get("mobile_no", False)
        website = request.POST.get("website", False)
        phone = request.POST.get("phone", False)
        email = request.POST.get("email", False)
        address = request.POST.get("address", False)

        try:
            logo = request.FILES['logo']
        except:
            logo = ""

        data_company = company_master.objects.get(id=company_id)
        if (data_company.company_name == companyname) and (data_company.tax_number == tax_no) and (data_company.mobile == mobile_no) and (data_company.website == website) and (data_company.phone == phone) and (data_company.email == email) and (data_company.address == address) and (logo == ""):
            messages.warning(request, "No changes !!!!!!!")
            return redirect(request.META['HTTP_REFERER'])
        elif (data_company.company_name == companyname):
            data = company_master.objects.filter(id=company_id).update(
                company_name=companyname,
                tax_number=tax_no,
                mobile=mobile_no,
                website=website,
                phone=phone,
                email=email,
                address=address,
                created_by=request.user,
                status="True"
            )
            try:
                fixed_height = 400
                image = Image.open(logo)
                print("image.size", image.size)
                width_size = int(fixed_height / image.height * image.width)
                print("width_size:::::", width_size)
                resized_image = image.resize((width_size, fixed_height))
                print("resizeeeeeed:", resized_image.size)
                from django.conf import settings
                resized_image.save("media/company_logo/" + logo.name, quality=100)
                image_new1 = 'company_logo/' + logo.name
                data_update = company_master.objects.filter(id=company_id).update(company_logo=image_new1)
            except:
                pass
        elif company_master.objects.filter(company_name=companyname).exists():
            messages.error(request,"Company name already exists")
            return redirect(request.META['HTTP_REFERER'])
        else:
            data = company_master.objects.filter(id=company_id).update(
                company_name=companyname,
                tax_number=tax_no,
                mobile=mobile_no,
                website=website,
                phone=phone,
                email=email,
                address=address,
                created_by=request.user,
                status="True"
            )
            try:
                fixed_height = 400
                image = Image.open(logo)
                print("image.size", image.size)
                width_size = int(fixed_height / image.height * image.width)
                print("width_size:::::", width_size)
                resized_image = image.resize((width_size, fixed_height))
                print("resizeeeeeed:", resized_image.size)
                from django.conf import settings
                resized_image.save("media/company_logo/" + logo.name, quality=100)
                image_new1 = 'company_logo/' + logo.name
                data_update = company_master.objects.filter(id=company_id).update(company_logo=image_new1)
            except:
                pass
        messages.success(request, "Updated company details")
        return redirect('company_management_new')



def company_delete_modal(request):
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        data = company_master.objects.get(id=company_id)
        data.delete()
        messages.success(request, "Company Deleted Successfully..")
        return redirect('company_management_new')
    else:
        id = request.GET.get("id")
        data = company_master.objects.get(id=id)
        return render(request,"company_delete_modal.html",{'data':data})






# -----------------------------------------------------user_management-----------------------------------------------------------------

def user_management_new(request):
    user_data = User.objects.all().first()
    member_data = User_details.objects.all().exclude(created_by=user_data)

    data = User_details.objects.all()
    company_data = company_master.objects.all()
    context = {
        "data": data,
        "member_data": member_data,
        "company_data":company_data
    }
    return render(request,"user_management_new.html",context)


def user_edit_modal(request):
    id = request.GET.get("id")
    user_data = User_details.objects.get(id=id)
    company_data = company_master.objects.all()
    context = {
        'user_data':user_data,
        'company_data':company_data
    }
    return render(request,"user_edit_modal.html",context)


def user_details_signup(request):
    username = request.GET.get("username",False)
    email_id = request.GET.get("email_id",False)
    phone_number  =  request.GET.get("phone_number",False)

    data = []
    if User.objects.filter(username=username).exists():
        data = {"message":"usernameTrue"}
        return JsonResponse(data,safe=False)
    
    
    elif User_details.objects.filter(email=email_id).exists():
        data = {"message":"emailTrue"}
        return JsonResponse(data,safe=False)
    
    elif len(phone_number) < 8 :
        data = {"message":"phoneTrue"}
        return JsonResponse(data,safe=False)
    
    else:
        data = {"message":"False"}
        return JsonResponse(data,safe=False)






def user_details_check(request):
    username = request.GET.get("username",False)
    password1 = request.GET.get("password2",False)
    password2 = request.GET.get("password3",False)
    email_id = request.GET.get("email_id",False)
    Automatic = request.GET.get("Automatic",False)
    phone_number  =  request.GET.get("phone_number",False)
    print("Automatic:",Automatic)

    data = []
    if User.objects.filter(username=username).exists():
        data = {"message":"usernameTrue"}
        return JsonResponse(data,safe=False)
    
    elif Automatic != "true":
        data = {"message":"hy"}
        if password1 != password2:
            data = {"message":"passwordTrue"}
            return JsonResponse(data,safe=False)
        elif password1 == "":
            data = {"message":"password_blankTrue"}
            return JsonResponse(data,safe=False)
        return JsonResponse(data,safe=False)
    
    
    elif User_details.objects.filter(email=email_id).exists():
        data = {"message":"emailTrue"}
        return JsonResponse(data,safe=False)
    
    elif len(phone_number) < 8 :
        data = {"message":"phoneTrue"}
        return JsonResponse(data,safe=False)
    
    else:
        data = {"message":"False"}
        return JsonResponse(data,safe=False)




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
    if User.objects.filter(username=data['username']).exists():
        messages.warning(request,"Username already exists")
        return redirect(request.META['HTTP_REFERER'])
    elif User_details.objects.filter(email=data['email']).exists():
        messages.warning(request,"Email already exists")
        return redirect(request.META['HTTP_REFERER'])
    elif len(data['phone']) < 8:
        messages.warning(request,"Phone number should be minimum 8 digits")
        return redirect(request.META['HTTP_REFERER'])
   
    else:

        # super_admin add company admin(navabsir)

        if data['user_type'] == "company_admin":

            if company_master.objects.filter(company_name = data['companyname']).exists():

                data1 = company_master.objects.get(company_name = data['companyname'])
                
                if User_details.objects.filter(company_id_id = data1.id,user_type = "company_admin"):
                    messages.warning(request,"Company admin already exist")
                    return redirect('user_management_new')
                    
                else:
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
                    name = data['name'].title(),
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
            return redirect('user_management_new')
            
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
                    name = data['name'].title(),
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
                    name = data['name'].title(),
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


@api_view(['POST'])
def edit_company_admin_user(request):
    data = request.data
    try:
        photo = request.FILES['photo']
    except:
        photo = ""
    user_data = User_details.objects.get(id=data['company_admin_id'])
    user_update = User.objects.get(username=data['username_old'])

    if user_update.username != data['username']:
        
        if User.objects.filter(username=data['username']).exists():
            messages.warning(request,"Username already exists")
            return redirect(request.META['HTTP_REFERER'])
        else:
            pass
    elif user_data.email != data['email']:
        if User_details.objects.filter(email=data['email']).exists():
            messages.warning(request,"Email already exists")
            return redirect(request.META['HTTP_REFERER'])
        else:
            pass
    elif data['password'] != data['confirm_password']:
        if data['password'] != data['confirm_password']:

            messages.warning(request,"password doesn't match")
            return redirect(request.META['HTTP_REFERER'])
        else:
            pass
    else:

        user_update.username = data['username']
        user_update.save()
        if (user_data.name == data['name']) and (user_data.company_name == data['companyname']) and (user_data.username == data['username']) and (user_data.phone == data['phone']) and (user_data.email == data['email']) and (photo == "") and (data['password_option'] == "no_change"):
            messages.warning(request, "No Updates !!!")
            return redirect(request.META['HTTP_REFERER'])
        elif (data['password'] != data['confirm_password']):
            messages.warning(request, "Password Doesnot Match !!!")
            return redirect(request.META['HTTP_REFERER'])
        elif(user_data.username == data['username']):
            data_user = User_details.objects.filter(id=data['company_admin_id']).update(
                name=data['name'],
                company_name=data['companyname'],
                username=data['username'],
                phone=data['phone'],
                email=data['email'],
            )
            if (data['password_option'] == "change_password"):
                user_update.set_password(data['password'])
                user_update.save()
                user_data_update = User_details.objects.filter(id=data['company_admin_id']).update(password=data['password'])
            else:
                pass
            try:
                fixed_height = 128
                image = Image.open(photo)
                print("image.size", image.size)
                width_size = int(fixed_height / image.height * image.width)

                resized_image = image.resize((width_size, fixed_height))
                print("resizeeeeeed:", resized_image.size)
                from django.conf import settings
                resized_image.save("media/user_image/" + photo.name)
                image_new1 = 'user_image/' + photo.name
                data_user = User_details.objects.filter(id=data['company_admin_id']).update(photo=image_new1)
            except:
                pass
        elif User_details.objects.filter(username=data['username']).exists():
            messages.warning(request,"Username already exists")
            return redirect(request.META['HTTP_REFERER'])
        else:
            data_user =User_details.objects.filter(id=data['company_admin_id']).update(
                name=data['name'],
                company_name=data['companyname'],
                username=data['username'],
                phone=data['phone'],
                email=data['email'],
            )
            if (data['password_option'] == "change_password"):
                user_update.set_password(data['password'])
                user_update.save()
                user_data_update = User_details.objects.filter(id=data['company_admin_id']).update(password=data['password'])
            else:
                pass
            try:
                fixed_height = 128
                image = Image.open(photo)
                print("image.size", image.size)
                width_size = int(fixed_height / image.height * image.width)

                resized_image = image.resize((width_size, fixed_height))
                print("resizeeeeeed:", resized_image.size)
                from django.conf import settings
                resized_image.save("media/user_image/" + photo.name)
                image_new1 = 'user_image/' + photo.name
                data_user = User_details.objects.filter(id=data['company_admin_id']).update(photo=image_new1)
            except:
                pass
        messages.success(request, "Successfully updated User details")
        return redirect('user_management_new')



def user_delete_modal(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        data = User_details.objects.get(id=user_id)
        auth_data = data.auth_user
        data.delete()
        auth_data.delete()
        messages.success(request, "User Deleted Successfully..")
        return redirect('user_management_new')
    else:
        id = request.GET.get("id")
        data = User_details.objects.get(id=id)
        return render(request,"user_delete_modal.html",{'data':data})



# -----------------------------------------------------member_management-----------------------------------------------------------------

def member_management(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    manager_data = ""
    role_data = ""
    try:
        user_details_data = User_details.objects.get(auth_user=request.user)
        role_data = Role_master.objects.filter(company_id = user_details_data.company_id.id)
        manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )
    except:
        pass


    user_permission_modal = user_permission_mapping.objects.filter(auth_user_id=request.user)
    user_permission_modal1 = list(user_permission_modal.values_list('role_mapping_id',flat=True))
    user_manage_all_permission = Role_mapping.objects.filter(role_master_id__in=user_permission_modal1,navbar_name="Team member",view_all=True)

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



def member_edit_modal(request):
    id = request.GET.get("id")
    user_data = User_details.objects.get(id=id)
    roles = user_permission_mapping.objects.filter(user_id=user_data)
    manager_data = ""
    role_data = ""
    try:
        user_details_data = User_details.objects.get(auth_user=request.user)
        role_data = Role_master.objects.filter(company_id=user_details_data.company_id.id)
        manager_data = User_details.objects.filter(user_level="Manager", company_id=user_details_data.company_id.id)
        print("manager_data:::::", manager_data)
    except:
        pass
    context = {
        'user_data':user_data,
        'manager_data':manager_data,
        'role_data':role_data,
        'roles':roles,
    }
    return render(request,"member_edit_modal.html",context)



@api_view(['POST'])
def memeber_edit_action(request):
    data = request.data
    role_id = request.POST.getlist("role_id[]")
    role_description = request.POST.getlist("role_description[]")
    role_start_dt = request.POST.getlist("role_start_dt[]")
    role_end_dt = request.POST.getlist("role_end_dt[]")
    role_permission_name = request.POST.getlist("role_permission_name")
    role_length = len(role_id)

    role_id_new = request.POST.getlist("role_id_new[]")
    role_description_new = request.POST.getlist("role_description_new[]")
    role_start_dt_new = request.POST.getlist("role_start_dt_new[]")
    role_end_dt_new = request.POST.getlist("role_end_dt_new[]")
    role_length_new = len(role_id_new)

    role_delete = request.POST.get("role_delete")
    aaaa = [int(x.strip()) for x in role_delete.split(',') if x]
    data_delete = user_permission_mapping.objects.filter(id__in=aaaa)
    data_delete.delete()

    try:
        photo = request.FILES['photo']
    except:
        photo = ""
    user_data = User_details.objects.get(id=data['member_id'])
    user_update = User.objects.get(username=data['username_old'])
    user_update.username = data['username']
    user_update.save()
   
    if(user_data.username == data['username']):
        data_user = User_details.objects.filter(id=data['member_id']).update(
            name=data['name'].title(),
            username=data['username'],
            phone=data['phone'],
            email=data['email'],
        )
        for i in range(0, role_length):
            role_end_dt1 = role_end_dt[i]
            if role_end_dt1 == "":
                role_end_dt1 = None
            data_save_user_role = user_permission_mapping.objects.filter(id=role_permission_name[i],user_id_id=data['member_id']).update(
                role_mapping_id_id=int(role_id[i]),
                start_dt=role_start_dt[i],
                end_dt=role_end_dt1,
                description=role_description[i]
            )
        for i in range(0, role_length_new):
            user = User.objects.get(username=data['username'])
            role_end_dt2 = role_end_dt_new[i]
            if role_end_dt2 == "":
                role_end_dt2 = None
            data_save_user_role = user_permission_mapping(
                auth_user_id_id=user.id,
                user_id_id=user_data.id,
                role_mapping_id_id=role_id_new[i],
                start_dt=role_start_dt_new[i],
                end_dt=role_end_dt2,
                description=role_description_new[i]
            )
            data_save_user_role.save()

        if (user_data.manager_auth.username == data['manager_id']):
            pass
        else:
            user_id = data['manager_id']

            user_detail = User_details.objects.get(id=user_id)
            data_user = User_details.objects.filter(id=data['member_id']).update(
            manager_auth_id = user_detail.auth_user.id)
        if (data['password_option'] == "change_pass"):
            user_update.set_password(data['password'])
            user_update.save()
            user_data_update = User_details.objects.filter(id=data['member_id']).update(password=data['password'])
        else:
            pass
        try:
            fixed_height = 128
            image = Image.open(photo)
            width_size = int(fixed_height / image.height * image.width)

            resized_image = image.resize((width_size, fixed_height))
            from django.conf import settings
            resized_image.save("media/user_image/" + photo.name)
            image_new1 = 'user_image/' + photo.name
            data_user = User_details.objects.filter(id=data['member_id']).update(photo=image_new1)
        except:
            pass
    elif User_details.objects.filter(username=data['username']).exists():
        messages.warning(request,"Username already exists")
        return redirect(request.META['HTTP_REFERER'])
    else:
        data_user =User_details.objects.filter(id=data['member_id']).update(
            name=data['name'].title(),
            username=data['username'],
            phone=data['phone'],
            email=data['email'],
        )
        if (user_data.manager_auth.username == data['manager_id']):
            pass
        else:
            user_id = data['manager_id']

            user_detail = User_details.objects.get(id=user_id)
            data_user = User_details.objects.filter(id=data['member_id']).update(
            manager_auth_id = user_detail.auth_user.id)
        if (data['password_option'] == "change_password"):
            user_update.set_password(data['password'])
            user_update.save()
            user_data_update = User_details.objects.filter(id=data['member_id']).update(password=data['password'])
        else:
            pass
        try:
            fixed_height = 128
            image = Image.open(photo)
            width_size = int(fixed_height / image.height * image.width)

            resized_image = image.resize((width_size, fixed_height))
            from django.conf import settings
            resized_image.save("media/user_image/" + photo.name)
            image_new1 = 'user_image/' + photo.name
            data_user = User_details.objects.filter(id=data['member_id']).update(photo=image_new1)
        except:
            pass
    messages.success(request, "Successfully updated Member details")
    return redirect('member_management')


def member_delete_modal(request):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        data = User_details.objects.get(id=member_id)
        data.delete()
        messages.success(request, "Memeber Deleted Successfully..")
        return redirect('member_management')
    else:
        id = request.GET.get("id")
        data = User_details.objects.get(id=id)
        return render(request,"member_delete_modal.html",{'data':data})




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


def edit_role_management(request):
    id = request.GET.get("id")
    role_data = Role_master.objects.get(id=id)
    role_role = Role_mapping.objects.get(role_master_id_id=role_data.id, navbar_name="Role")
    role_team = Role_mapping.objects.get(role_master_id_id=role_data.id, navbar_name="Team member")
    role_tags = Role_mapping.objects.get(role_master_id_id=role_data.id, navbar_name="Tags")
    role_status = Role_mapping.objects.get(role_master_id_id=role_data.id, navbar_name="Status")
    context = {
        'role_data':role_data,
        'role_role': role_role,
        'role_team': role_team,
        'role_tags': role_tags,
        'role_status': role_status,
    }
    return render(request, "edit_role_management.html", context)



def delete_role_management(request):
    if request.method == "POST":
        role_id = request.POST.get("role_id")
        data = Role_master.objects.get(id=role_id)
        data.delete()
        messages.success(request, "Role Deleted Successfully..")
        return redirect('role_management')
    else:
        id = request.GET.get("id")
        data = Role_master.objects.get(id=id)
        return render(request,"delete_role_management.html",{'data':data})


def edit_role_action(request):
    if request.method == "POST":
        role_data = request.POST.get('role_data')
        role_role = request.POST.get('role_role')
        role_team = request.POST.get('role_team')
        role_tags = request.POST.get('role_tags')
        role_status = request.POST.get('role_status')

        data_role = Role_master.objects.get(id=role_data)
        data_role_role = Role_mapping.objects.get(id=role_role)
        data_role_team = Role_mapping.objects.get(id=role_team)
        data_role_tag = Role_mapping.objects.get(id=role_tags)
        data_role_status = Role_mapping.objects.get(id=role_status)

        if ((data_role.role_name == request.POST.get('name')) and (data_role.description == request.POST.get('description')) and (str(data_role_role.read) == str(request.POST.get('role_read',False))) and (str(data_role_role.write) == str(request.POST.get('role_write',False))) and (str(data_role_role.edit) == str(request.POST.get('role_edit',False))) and (str(data_role_role.delete) == str(request.POST.get('role_delete',False))) and (str(data_role_role.view_all) == str(request.POST.get('role_view_all',False))) and (str(data_role_role.manage_all) == str(request.POST.get('role_manage_all',False))) and (str(data_role_team.read) == str(request.POST.get('team_member_read',False))) and (str(data_role_team.write) == str(request.POST.get('team_member_write',False))) and (str(data_role_team.edit) == str(request.POST.get('team_member_edit',False))) and (str(data_role_team.delete) == str(request.POST.get('team_member_delete',False))) and (str(data_role_team.view_all) == str(request.POST.get('team_member_view_all',False))) and (str(data_role_team.manage_all) == str(request.POST.get('team_member_manage_all',False))) and (str(data_role_tag.read) == str(request.POST.get('tag_read',False))) and (str(data_role_tag.write) == str(request.POST.get('tag_write',False))) and (str(data_role_tag.edit) == str(request.POST.get('tag_edit',False))) and (str(data_role_tag.delete) == str(request.POST.get('tag_delete',False))) and (str(data_role_tag.view_all) == str(request.POST.get('tag_view_all',False))) and (str(data_role_tag.manage_all) == str(request.POST.get('tag_manage_all',False))) and (str(data_role_status.read) == str(request.POST.get('status_read',False))) and (str(data_role_status.write) == str(request.POST.get('status_write',False))) and (str(data_role_status.edit) == str(request.POST.get('status_edit',False))) and (str(data_role_status.delete) == str(request.POST.get('status_delete',False))) and (str(data_role_status.view_all) == str(request.POST.get('status_view_all',False))) and (str(data_role_status.manage_all) == str(request.POST.get('status_manage_all',False)))):
            messages.warning(request, "No Updates...!!")
            return redirect('role_management')
        else:
            data_save_role = Role_master.objects.filter(id=role_data).update(
                    role_name = request.POST.get('name'),
                    description = request.POST.get('description'),
                )

            Role_mapping.objects.filter(id=role_role).update(
                    navbar_name = "Role",
                    read = request.POST.get('role_read',False),
                    write = request.POST.get('role_write',False),
                    edit = request.POST.get('role_edit',False),
                    delete = request.POST.get('role_delete',False),
                    view_all = request.POST.get('role_view_all',False),
                    manage_all = request.POST.get('role_manage_all',False),
                )

            Role_mapping.objects.filter(id=role_team).update(
                    navbar_name = "Team member",
                    read = request.POST.get('team_member_read',False),
                    write = request.POST.get('team_member_write',False),
                    edit = request.POST.get('team_member_edit',False),
                    delete = request.POST.get('team_member_delete',False),
                    view_all = request.POST.get('team_member_view_all',False),
                    manage_all = request.POST.get('team_member_manage_all',False),
                )


            Role_mapping.objects.filter(id=role_tags).update(
                    navbar_name = "Tags",
                    read = request.POST.get('tag_read',False),
                    write = request.POST.get('tag_write',False),
                    edit = request.POST.get('tag_edit',False),
                    delete = request.POST.get('tag_delete',False),
                    view_all = request.POST.get('tag_view_all',False),
                    manage_all = request.POST.get('tag_manage_all',False),
                )

            Role_mapping.objects.filter(id=role_status).update(
                    navbar_name = "Status",
                    read = request.POST.get('status_read',False),
                    write = request.POST.get('status_write',False),
                    edit = request.POST.get('status_edit',False),
                    delete = request.POST.get('status_delete',False),
                    view_all = request.POST.get('status_view_all',False),
                    manage_all = request.POST.get('status_manage_all',False),
                )

            messages.success(request,"Successfully updated Role")
            return redirect('role_management')



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



def task_edit_modal(request):
    id = request.GET.get("id")
    task_data = status_name_master.objects.get(id=id)

    context = {
        'task_data':task_data,
    }
    return render(request, "task_edit_modal.html", context)


def task_delete_modal(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        data = status_name_master.objects.get(id=task_id)
        data.delete()
        messages.success(request, "Task Deleted Successfully..")
        return redirect('task_status_management')
    else:
        id = request.GET.get("id")
        data = status_name_master.objects.get(id=id)
        return render(request,"task_delete_modal.html",{'data':data})


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

@api_view(['POST'])
def task_edit_action(request):
    data = request.data
    data_task = status_name_master.objects.get(id=data['task_id'])
    if (data_task.status_name==data['status_name']) and (data_task.status_color==data['status_color']):
        messages.warning(request, "No Updates")
        return redirect('task_status_management')
    else:
        data_update = status_name_master.objects.filter(id=data['task_id']).update(status_name = data['status_name'],status_color=data['status_color'])
        messages.success(request,"Successfully updated Status")
        return redirect('task_status_management')




# ----------------------------------------------------project_management-------------------------------------------------------------

def project_management(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    user_details_data = User_details.objects.get(auth_user = request.user)
    member_data = User_details.objects.filter(company_id =user_details_data.company_id)
    manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )

    status_name = status_name_master.objects.filter(company_id=user_details_data.company_id)

    space_master_data = ""
    sub_space_data =""
    space_dept = ""
    try:
        userdetails_data = User_details.objects.get(auth_user=request.user)

        # if user is company_admin (navab sir (all space of him))
        if userdetails_data.user_type == "company_admin":
            space_master_data = space_master.objects.filter(added_user_id=request.user)
            space_list = list(space_master_data.values_list('id',flat=True))
            space_dept = space_master.objects.get(id=space_list[0])
            sub_space_data = sub_space_master.objects.filter(space_id =space_list[0])
        else:
            # if user is company_user(their space only)
            sub_space = sub_space_master.objects.filter(invite_user_auth_id=request.user)
            user_permission_space = list(sub_space.values_list('space_id',flat=True))
            space_master_data = space_master.objects.filter(id__in=user_permission_space)

            space_list = list(space_master_data.values_list('id',flat=True))
            space_dept = space_master.objects.get(id=space_list[0])
            sub_space_data = sub_space_master.objects.filter(space_id =space_list[0])

    except:
        pass
   
   

    context = {
    "member_data" : member_data,
    "user_details_data":user_details_data,
    "status_name":status_name,
    "manager_data":manager_data,
    "space_master_data":space_master_data,
    "sub_space_data":sub_space_data,
    "space_dept":space_dept,
    "today_date":today_date
    }
    return render(request, 'project_management.html',context)


# -----------------------------------------------------space_management-----------------------------------------------------------------

def edit_group_modal(request):
    space_id = request.GET.get("space_id")
    print("space_id::::::::",space_id)
    space_data = space_master.objects.get(id=space_id)

    context = {
        'space_data':space_data,
    }
    return render(request, "edit_group_modal.html", context)


def space_edit_action(request):
    if request.method == "POST":
        spacename = request.POST.get("spacename",False)
        group_name = spacename.title()
        space_id = request.POST.get("space_id",False)
        space_master.objects.filter(id=space_id).update(space_name =group_name)
        messages.success(request,"Successfully updated Group")
        return redirect(request.META['HTTP_REFERER'])


def space_add_action(request):
    if request.method == "POST":
        spacename = request.POST.get("spacename",False)
        group_name = spacename.title()
        task_status_add = request.POST.getlist("task_status_add",False)
        print("task_status_add::::::",task_status_add)
        new_task_status_add = list(filter(None, task_status_add))
        if new_task_status_add:
            
            for t in new_task_status_add:
                user_data = User_details.objects.get(auth_user = request.user)
                status_name_master.objects.create(active_user_id_id =user_data.id,
                active_auth_user_id_id =request.user.id ,status_name = t,created_by = request.user,status="True",
                company_id_id = user_data.company_id.id )

        
        task_status_id = request.POST.getlist("task_status_name")
        task_status_data = status_name_master.objects.filter(id__in=task_status_id)
        task_status_list = list(task_status_data.values_list('id',flat=True))

        task_new_status_data =status_name_master.objects.filter(status_name__in=new_task_status_add)
        task_new_status_list = list(task_new_status_data.values_list('id',flat=True))

        status_list = task_status_list + task_new_status_list
        new_status = [*set(status_list)]

        user_data = User_details.objects.get(auth_user = request.user)
        if user_data.user_type == "company_admin":
            space_master_data = space_master.objects.create(space_name=group_name,
            added_user_id = request.user,
            status = "True",
            created_by = request.user
            )
            for k in new_status:
                space_master_data.task_status.add(k)

        else:
            user_active = user_active_account.objects.get(user_id=user_data.id)
            space_master_data = space_master.objects.create(space_name=group_name,
            active_account_id_id=user_active.active_user_id.id,
            added_user_id = request.user,
            status = "True",
            created_by = request.user
            )

            for k in new_status:
                space_master_data.task_status.add(k)
        messages.success(request,"Successfully added Group")
        return redirect('project_management')

def get_bucket_details(request):
    space_id = request.GET.get("space_id")
    space_data = space_master.objects.get(id=space_id)
    return render(request,'get_bucket_details.html',{"bucket_data":space_data.task_status.all()})


def project_add_action(request):
    if request.method == "POST":
        today_date = datetime.today().strftime('%Y-%m-%d')
        space_id = request.POST.get("space_id")
        foldername = request.POST.get("foldername")
        project_name = foldername.title()
       
        member_data = request.POST.getlist("member_data",False)
        manager_id = request.POST.getlist("manager_id",False)
        list_new = manager_id + member_data
        permission_user = [*set(list_new)]
        manager = request.POST.get("manager_id",False)
        User_details_data = User_details.objects.get(id=manager)
        
        notes = request.POST.get("notes",False)
        bucket = request.POST.get("bucket",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        planning_start_date = request.POST.get("planning_start_date",False)
        planning_end_date = request.POST.get("planning_end_date",False)
        actual_start_date = request.POST.get("actual_start_date",False)
        actual_end_date = request.POST.get("actual_end_date",False)
        comments = request.POST.get("comments",False)
        try:

            checklist_item = request.POST.getlist("checklist",False)
            new_checklist_item = list(filter(None, checklist_item))
            checklist_end_date = request.POST.getlist("checklist_end_date",False)
            new_checklist_end_date = list(filter(None, checklist_end_date))
        except:
            pass
        
        user_data = User_details.objects.get(auth_user = request.user)
        if user_data.user_type == "company_admin":
            data_save = sub_space_master.objects.create(space_id_id = space_id,
            sub_space_name = project_name,
            bucket_mapping_id_id = bucket,
            progress = progress,
            priority = priority,
            notes = notes,
            Planning_start_date = planning_start_date,
            Planning_end_date = planning_end_date,
            Actual_start_date = actual_start_date,
            Actual_end_date = actual_end_date,
            sub_space_manager_id = User_details_data.auth_user.id,
            added_user_id = request.user,
            created_by = request.user,status="True")

            for r in permission_user:
                user_details = User_details.objects.get(id=r)
                data_save.invite_user_auth_id.add(user_details.auth_user.id)
                data_save.invite_user_details_id.add(r)


            zip_objects = zip(new_checklist_item,new_checklist_end_date)

            for m,d in zip_objects:
                check_data = sub_space_checklist.objects.create(sub_space_id_id=data_save.id,
                milestone = m,due_date = d,updated_by = request.user,updated_dt=today_date)
           

               
            try:

                attached_file =  request.FILES.getlist('attached_file')
                print("attached_file:",attached_file)
                for i in attached_file:

                    import os
                    filename = os.path.splitext(str(i))[0]
                    extension = os.path.splitext(str(i))[1]
                    sub_space_attachment.objects.create(sub_space_id_id=data_save.id,
                    file_name = filename,file_type =extension ,attached_file = i,added_by = request.user)

            except:
                pass
                

            user_data = User_details.objects.get(auth_user=request.user)
            if comments == "":
                pass
            else:

                sub_space_comments.objects.create(sub_space_id_id=data_save.id,
                added_by_id = user_data.id,user_auth_id_id =request.user.id ,comments = comments)

        else:
            user_active = user_active_account.objects.get(user_id=user_data.id)

            data_save = sub_space_master.objects.create(space_id_id = space_id,
            sub_space_name = project_name,
            bucket_mapping_id_id = bucket,
            progress = progress,
            priority = priority,
            notes = notes,
            Planning_start_date = planning_start_date,
            Planning_end_date = planning_end_date,
            Actual_start_date = actual_start_date,
            Actual_end_date = actual_end_date,
            sub_space_manager_id = User_details_data.auth_user.id,
            active_account_id_id = user_active.active_user_id.id,
            added_user_id = request.user,
            created_by = request.user,status="True")

            for r in permission_user:
                user_details = User_details.objects.get(id=r)
                data_save.invite_user_auth_id.add(user_details.auth_user.id)
                data_save.invite_user_details_id.add(r)

            zip_objects = zip(new_checklist_item,new_checklist_end_date)

            for m,d in zip_objects:
                check_data = sub_space_checklist.objects.create(sub_space_id_id=data_save.id,
                milestone = m,due_date = d,updated_by = request.user,updated_dt=today_date)

            try:

                attached_file =  request.FILES.getlist('attached_file')
                print("attached_file:",attached_file)
                for i in attached_file:
                    import os
                    filename = os.path.splitext(str(i))[0]
                    extension = os.path.splitext(str(i))[1]
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

        messages.success(request,"Successfully added Project")
        return redirect(request.META['HTTP_REFERER'])


from django.http import HttpResponseRedirect
def update_project_details(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime("%H:%M:%S")
    print("current_time::;",current_time)
    if request.method == "POST":
        sub_space_id = request.POST.get("sub_space_id",False)
        project_name1 = request.POST.get("project_name",False)
        project_name = project_name1.title()
        tag_name = request.POST.getlist("tag_name",False)
        print("tag_name1:::::;",tag_name)
        
        
        status_name = request.POST.get("status_name",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        planning_start_date = request.POST.get("planning_start_date",False)
        planning_end_date = request.POST.get("planning_end_date",False)
        actual_start_date = request.POST.get("actual_start_date",False)
        actual_end_date = request.POST.get("actual_end_date",False)
        notes = request.POST.get("notes",False)
        checklist_new = request.POST.getlist("checklist_new",False)
        checklist_end_date = request.POST.getlist("checklist_date",False)
        
        try :

            checklist_new = list(filter(None, checklist_new))
            new_checklist_end_date = list(filter(None, checklist_end_date))
            print("new_checklist_end_date::::",new_checklist_end_date)
        except:
            pass

        try:

            checkbox_checklist = request.POST.get("checkbox_checklist",False)
            print('checkbox_checklist:',checkbox_checklist)
            sub_space_checklist.objects.filter(id=checkbox_checklist).update(status=True,updated_by = request.user,updated_dt=today_date,updated_tm =current_time)
        except:
            pass

        try:
            removed_user = request.POST.getlist("remove_assign_user[]",False)
            for i in removed_user:

                user_details = User_details.objects.get(id=i)
                data_save = sub_space_master.objects.get(id=sub_space_id)
                data_save.invite_user_auth_id.remove(user_details.auth_user.id)
                data_save.invite_user_details_id.remove(i)

        except:
            pass

        try:
            add_user = request.POST.getlist("add_new_memember_list",False)
            for i in add_user:

                user_details = User_details.objects.get(id=i)
                data_save = sub_space_master.objects.get(id=sub_space_id)
                data_save.invite_user_auth_id.add(user_details.auth_user.id)
                data_save.invite_user_details_id.add(i)
        except:
            pass

        try:

            attachment_new =  request.FILES.getlist('attachment_new')
            attach_name = request.POST.get("attach_name",False)
            print("attachment_new:",attachment_new)
            for i in attachment_new:
                import os
                filename = os.path.splitext(str(i))[0]
                print("nameeeee",filename)
                extension = os.path.splitext(str(i))[1]
                print("extension:",extension)
                file_type = "file"
                sub_space_attachment.objects.create(sub_space_id_id=sub_space_id,text_content = attach_name,
                file_name = filename,file_type =file_type ,attached_file = i,added_by = request.user)
        except:
            pass

        try:
            link_address = request.POST.get("link_address",False)
            text_content = request.POST.get("text_content",False)
            file_type = "link"
            sub_space_attachment.objects.create(sub_space_id_id=sub_space_id,text_content = text_content,
            file_name =link_address, file_type =file_type ,attached_file = link_address,added_by = request.user)
        except:
            pass

        sub_space_master.objects.filter(id=sub_space_id).update(sub_space_name = project_name,bucket_mapping_id =status_name,progress=progress,priority=priority,Planning_start_date=planning_start_date,Planning_end_date=planning_end_date,
        Actual_start_date = actual_start_date,Actual_end_date = actual_end_date,notes = notes,updated_dt = today_date)

        try:
            zip_objects = zip(checklist_new,new_checklist_end_date)
            for m,d in zip_objects:
                sub_space_checklist.objects.create(sub_space_id_id=sub_space_id,
                milestone = m,due_date = d,updated_by = request.user,updated_dt=today_date)
        except:
            pass
               
        sub_space = sub_space_master.objects.get(id=sub_space_id)
        sub_space.tag_id.clear()
        for t in tag_name:
            if t == '0':
                pass
            else:                
                sub_space.tag_id.add(t)

        try:

            remove_attachment = request.POST.getlist("remove_attachment[]",False)

            for i in remove_attachment:
                sub_space_attachment.objects.get(id=i).delete()
        except:
            pass

        messages.success(request,"Successfully updated Project details")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def update_task_details(request):
    if request.method == "POST":
        today_date = datetime.today().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime("%H:%M:%S")
        task_id = request.POST.get("task_id",False)
        task_name = request.POST.get("task_name",False)
        print("task_name:::::",task_name)
        tag_name = request.POST.getlist("tag_name",False)
        
        status_name = request.POST.get("status_name",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        start_date = request.POST.get("start_date",False)
        end_date = request.POST.get("end_date",False)
        notes = request.POST.get("notes",False)
        try:

            checklist_new = request.POST.getlist("checklist_new",False)
            checklist_new = list(filter(None, checklist_new))
            checklist_end_date = request.POST.getlist("checklist_date",False)
            new_checklist_end_date = list(filter(None, checklist_end_date))
        except:
            pass

        try:

            checkbox_checklist = request.POST.get("checkbox_checklist",False)
            print("checkbox_checklist:::::::",checkbox_checklist)
            Add_task_checklist.objects.filter(id=checkbox_checklist).update(status=True,updated_by = request.user,updated_dt=today_date,updated_tm =current_time)

        except:
            pass



        try:
            removed_user = request.POST.getlist("remove_assign_user[]",False)
            for i in removed_user:

                user_details = User_details.objects.get(id=i)
                data_save = Add_task_master.objects.get(id=task_id)
                data_save.invite_user_auth_id.remove(user_details.auth_user.id)
                data_save.invite_user_details_id.remove(i)

        except:
            pass



        try:
            add_user = request.POST.getlist("add_new_memember_list",False)
            for i in add_user:

                user_details = User_details.objects.get(id=i)
                data_save = Add_task_master.objects.get(id=task_id)
                data_save.invite_user_auth_id.add(user_details.auth_user.id)
                data_save.invite_user_details_id.add(i)
        except:
            pass


        try:

            attachment_new =  request.FILES.getlist('attachment_new')
            attach_name = request.POST.get("attach_name",False)
            print("attachment_new:",attachment_new)
            for i in attachment_new:

                import os
                filename = os.path.splitext(str(i))[0]
                print("nameeeee",filename)
                extension = os.path.splitext(str(i))[1]
                print("extension:",extension)
                file_type = "file"
                Add_task_attachment.objects.create(add_task_id_id=task_id,text_content = attach_name,
                file_name = filename,file_type =file_type ,attached_file = i,added_by = request.user)
        except:
            pass


        try:
            link_address = request.POST.get("link_address",False)
            text_content = request.POST.get("text_content",False)
            file_type = "link"
            Add_task_attachment.objects.create(add_task_id_id=task_id,text_content = text_content,
            file_name =link_address, file_type =file_type ,attached_file = link_address,added_by = request.user)
        except:
            pass


        today_date = datetime.today().strftime('%Y-%m-%d')
        Add_task_master.objects.filter(id=task_id).update(task_name = task_name,bucket_mapping_id =status_name,progress=progress,priority=priority,start_date=start_date,end_date=end_date,
        notes = notes,updated_dt = today_date)

       
        try:
            zip_objects = zip(checklist_new,new_checklist_end_date)
            for m,d in zip_objects:
                Add_task_checklist.objects.create(add_task_id_id=task_id,
                item_name = m,due_date = d,updated_by = request.user,updated_dt=today_date)
        except:
            pass

        add_task = Add_task_master.objects.get(id=task_id)
        add_task.tag_id.clear()
        for t in tag_name:
            if t == '0':
                pass
            else:                
                add_task.tag_id.add(t)

        try:

            remove_attachment = request.POST.getlist("remove_attachment[]",False)

            for i in remove_attachment:
                Add_task_attachment.objects.get(id=i).delete()
        except:
            pass



        messages.success(request,"Successfully updated Task details")
        return redirect(request.META['HTTP_REFERER'])


def view_group(request):
    space_id = request.GET.get("space_id")
    space_data = space_master.objects.get(id=space_id)
    today_date = datetime.today().strftime('%Y-%m-%d')


    user_details_data = User_details.objects.get(auth_user=request.user)
    
    sub_space_data = sub_space_master.objects.filter(space_id=space_id)

    context={
        "space_data":space_data,
        "today_date":today_date,
        "sub_space_data":sub_space_data
    }
    return render(request, 'view_group.html',context)



def view_project_page(request):
    from.models import progress,priority
    from datetime import datetime
    today_date = datetime.today().strftime('%Y-%m-%d')

    sub_space_id = request.GET.get("sub_space_id")
    sub_space_data = sub_space_master.objects.get(id=sub_space_id)
    manager_of_project = sub_space_data.sub_space_manager
    user_details_manger = User_details.objects.get(auth_user=manager_of_project)

    space_id = sub_space_data.space_id
    space_data = space_master.objects.get(id=space_id.id)

    task_data = Add_task_master.objects.filter(space_id = space_id,sub_space_id = sub_space_id,parent_id = None)

    user_details_data = User_details.objects.get(auth_user=request.user)
    dynamic_status = status_name_master.objects.filter(company_id=user_details_data.company_id)    
    tags_name = tags_name_master.objects.filter(company_id=user_details_data.company_id) 

    time_details = ""
    total_hr = ""

    task_data_time = Add_task_master.objects.filter(space_id = space_id,sub_space_id = sub_space_id)
    task_details = list(task_data_time.values_list('id',flat=True))
    if user_details_data.user_type == "company_admin":
        print("user is company admin:")

        user_active_account1 = user_active_account.objects.filter(active_auth_user_id =request.user)
        child_user_id = list(user_active_account1.values_list('user_id__auth_user',flat=True))
        child_user_id.append(int(request.user.id))
        
        member_data = User_details.objects.filter(created_by__in=child_user_id) 
        member_data9 = list(member_data.values_list('auth_user',flat=True))
        # member_data1 = User_details.objects.filter(auth_user=request.user) 
        # member_data = list(chain(member_data1,member_data))
        print("member_data:",member_data)
        

        time_details = Task_time_details.objects.filter(task_id__in=task_details,user_auth_id__in = member_data9)
        print("time_details::::555555555555555::::::",time_details)
        total_hr = ""
        try : 
            total_price = sum(time_details.values_list('total_second', flat=True))
            total_hr = convert(total_price)
        except:
            pass

        
            

    user_data = User_details.objects.get(auth_user = request.user)
    member_data = User_details.objects.filter(company_id =user_data.company_id)
    

    user_access_generate = Project_user_access_link.objects.filter(project_id_id=sub_space_id).first()
    tag_selected_instance = list(sub_space_data.tag_id.all().values_list('id',flat=True))
    tag_selected_instance.insert(0, 0)
    
    context = {
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
        "time_details":time_details,
        "total_hr":total_hr,
        'user_access_generate':user_access_generate,
        "member_data":member_data,
        "tag_data": tag_selected_instance,
        "user_details_manger":user_details_manger
       
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
        task_name1 = request.POST.get("task_name",False)
        task_name = task_name1.title()

        notes = request.POST.get("notes",False)
        bucket = request.POST.get("bucket",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        start_date = request.POST.get("start_date",False)
        end_date = request.POST.get("end_date",False)
        try:

            checklist_item = request.POST.getlist("checklist",False)
            new_checklist_item = list(filter(None, checklist_item))
            checklist_end_date = request.POST.getlist("checklist_end_date",False)
            new_checklist_end_date = list(filter(None, checklist_end_date))
        except:
            pass
        comments = request.POST.get("comments",False)
        print("comments::::::",comments)

        task_master_save = Add_task_master.objects.create(space_id_id = space_id,
        sub_space_id_id = sub_space_id,
        task_name = task_name,
        bucket_mapping_id_id = bucket,
        progress = progress,
        priority = priority,
        notes = notes,
        start_date = start_date,
        end_date = end_date,
        task_status = "Main_task",
        created_by = request.user
        )


        for i in member_checkbox:
            user_details = User_details.objects.get(id=i)
            task_master_save.invite_user_auth_id.add(user_details.auth_user.id)
            task_master_save.invite_user_details_id.add(i)

            
            

        zip_objects = zip(new_checklist_item,new_checklist_end_date)

        today_date = datetime.today().strftime('%Y-%m-%d')
        for m,d in zip_objects:
            Add_task_checklist.objects.create(add_task_id_id=task_master_save.id,
            item_name = m,due_date = d,updated_by = request.user,updated_dt=today_date)

        

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
        if comments == "":
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
    parent_id = request.GET.get("parent_id")
   
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

  
    user_details_data = User_details.objects.get(auth_user=request.user)
    dynamic_status = status_name_master.objects.filter(company_id=user_details_data.company_id)    
    tags_name = tags_name_master.objects.filter(company_id=user_details_data.company_id) 


    status =  request.GET.get("status")
    if status == "task":
        suggestion_user = sub_space_master.objects.get(id=sub_space_data.id)
        pass
    else:
        suggestion_user = Add_task_master.objects.get(id=parent_id)
        pass

    tag_selected_instance = list(task_data.tag_id.all().values_list('id',flat=True))
    tag_selected_instance.insert(0, 0)



    context = {
        "space_data":space_data,
        "sub_space_data":sub_space_data,
        "task_data":task_data,
        "today_date":today_date,
        "bucket_data":space_data.task_status.all(),
        "progress":progress,
        "priority":priority,
        "today_date":today_date,
        "sub_task_data":sub_task_data,
        "dynamic_status":dynamic_status,
        "tags_name":tags_name,

        "current_status":current_status,
        "button_status":button_status,
        "refresh_time_diff":refresh_time_diff,
        "time_details":time_details,
        'total_hr':total_hr,
        'parent_id':parent_id,
        'suggestion_user':suggestion_user,
        'task_id':task_id,
        "tag_data": tag_selected_instance
      
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
        parent_id = request.POST.get("parent_id")
        member_checkbox = request.POST.getlist("member_checkbox")
        sub_task_name1 = request.POST.get("sub_task_name",False)
        sub_task_name = sub_task_name1.title()
        notes = request.POST.get("notes",False)
        bucket = request.POST.get("bucket",False)
        progress = request.POST.get("progress",False)
        priority = request.POST.get("priority",False)
        start_date = request.POST.get("start_date",False)
        end_date = request.POST.get("end_date",False)  

        sub_task_master_save = Add_task_master.objects.create(space_id_id = space_id,sub_space_id_id = sub_space_id,parent_id_id = task_id,
        task_name =sub_task_name,
        bucket_mapping_id_id=bucket,
        progress = progress,
        priority = priority,
        notes = notes,
        start_date = start_date,
        end_date = end_date,
        task_status = "sub_task",
        created_by = request.user
        )
        task_list = []
        def check(parent_id):
            task_list.append(parent_id)
            task_previous_data =  Add_task_master.objects.get(id=parent_id)  
            if task_previous_data.parent_id:
                prev_pid = task_previous_data.parent_id
                check(prev_pid.id)
            else:
                pass
            return task_list
        
        check(task_id)
        print("task_lisffft:::::",task_list)
        # task_list.sort()
        # print("sorted_list:::::",task_list.sort())

        
        sub_task_data = Add_task_master.objects.get(id=sub_task_master_save.id)
        for i in task_list:
            sub_task_data.multiple_parent_id.add(i)

        for i in member_checkbox:
            user_details = User_details.objects.get(id=i)
            sub_task_master_save.invite_user_auth_id.add(user_details.auth_user.id)
            sub_task_master_save.invite_user_details_id.add(i)
        messages.success(request,"Successfully added Sub Task")
        return redirect(request.META['HTTP_REFERER'])


# -----------------------------------------------------tags_management-----------------------------------------------------------------

def tags_management(request):
    
    user_details_data = User_details.objects.get(auth_user=request.user)
    tags_name = tags_name_master.objects.filter(company_id=user_details_data.company_id)    

    context = {
        
        "tags_name":tags_name,
        "user_details_data":user_details_data
    }
    return render(request, 'tags_management.html',context)


def tag_edit_modal(request):
    id = request.GET.get("id")
    tag_data = tags_name_master.objects.get(id=id)

    context = {
        'tag_data':tag_data,
    }
    return render(request, "tag_edit_modal.html", context)


def tag_delete_modal(request):
    if request.method == "POST":
        tag_id = request.POST.get("tag_id")
        data = tags_name_master.objects.get(id=tag_id)
        data.delete()
        messages.success(request, "Tags Deleted Successfully..")
        return redirect('tags_management')
    else:
        id = request.GET.get("id")
        data = tags_name_master.objects.get(id=id)
        return render(request,"tag_delete_modal.html",{'data':data})



@api_view(['POST'])
def tags_add_action(request):
    data = request.data
    user_data = User_details.objects.get(auth_user = request.user)
    tags_name_master.objects.create(active_user_id_id =user_data.id,
    active_auth_user_id_id =request.user.id ,tags_name = data['tags_name'],created_by = request.user,status="True",
    tags_color=data['tags_color'],company_id_id = user_data.company_id.id )
    messages.success(request,"Successfully added Tags")
    return redirect('tags_management')


@api_view(['POST'])
def edit_tag_action(request):
    data = request.data
    data_tag = tags_name_master.objects.get(id=data['tag_id'])
    if (data_tag.tags_name==data['tags_name']) and (data_tag.tags_color==data['tags_color']):
        messages.warning(request, "No Updates")
        return redirect('tags_management')
    else:
        data_update = tags_name_master.objects.filter(id=data['tag_id']).update(tags_name=data['tags_name'],tags_color=data['tags_color'])
        messages.success(request, "Successfully updated Tags")
        return redirect('tags_management')


def new_tags(request):
    user_details_data = User_details.objects.get(auth_user=request.user)
    context={
        "user_details_data":user_details_data,
    }
    return render(request, 'new_tags.html',context)


def project_management_board(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    user_details_data = ""
    manager_data = ""
    try:

        user_details_data = User_details.objects.get(auth_user=request.user)
        member_data = User_details.objects.filter(company_id =user_details_data.company_id)
        manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id)
        status_name = status_name_master.objects.filter(company_id=user_details_data.company_id)
    
    except:
        pass
    space_id =  request.GET.get("space_id")
    space_datas = ""
    data_model = ""
    try:
        space_datas = space_master.objects.get(id=space_id)
    except:
        pass

    space_master_data = ""
    try:
        userdetails_data = User_details.objects.get(auth_user=request.user)

        # if user is company_admin (navab sir (all space of him))
        if userdetails_data.user_type == "company_admin":
            space_master_data = space_master.objects.get(id=space_id)
           
        else:
            # if user is company_user(their space only)
            space_master_data = space_master.objects.get(id=space_id)
    except:
        pass

    try:
        space_model = space_master.objects.get(id=space_id)
        status_model_data =list(space_model.task_status.values_list('id',flat=True))
        queryset = status_name_master.objects.filter(id__in=status_model_data)
        data_model = status_name_master_Serailzer(queryset,many=True,context={'space_id':space_id}).data
    except:
        pass

    context = {
    "user_details_data":user_details_data,
    "space_master_data":space_master_data,
    "today_date":today_date,
    "space_datas":space_datas,
    "data_model":data_model,
    "manager_data":manager_data,
    "member_data":member_data,
    "status_name":status_name
    }
    return render(request, 'project_management_board.html',context)


def get_group_details(request):

    today_date = datetime.today().strftime('%Y-%m-%d')
    space_id = request.GET.get("space_id")
    space_dept = space_master.objects.get(id=space_id)
    sub_space_data = sub_space_master.objects.filter(space_id=space_id)

    user_details_data = User_details.objects.get(auth_user=request.user)
    manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )
    member_data = User_details.objects.filter(company_id =user_details_data.company_id)

    context = {
        "today_date":today_date,
        "sub_space_data":sub_space_data,
        "space_dept":space_dept,
        "manager_data":manager_data,
        "member_data":member_data

    }
    return render(request,'get_group_details.html',context)



def project_tree_structure(request):
    sub_space_id = request.GET.get("project_id")
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
    
    if request.method == "POST":

        print("tttttttttttttttttttttttttttttttttttttt")
        project_id = request.POST.get("project_id")
        status_id = request.POST.get("status_id")
        data_update = sub_space_master.objects.filter(id=project_id).update(bucket_mapping_id_id=status_id)
        messages.success(request,str("Status updated"))
        return redirect(request.META['HTTP_REFERER'])


def update_task_status(request):
    if request.method == "POST":

        task_id = request.POST.get("task_id")
        print("task_id:::::::",task_id)
        status_id = request.POST.get("status_id")
        print("status_id:::::",status_id)
        data_update = Add_task_master.objects.filter(id=task_id).update(bucket_mapping_id_id=status_id)
        messages.success(request,str("Status updated"))
        return redirect(request.META['HTTP_REFERER'])



def get_project_comment(request):
    sub_space_id = request.GET.get("sub_space_id")
    comments = request.GET.get("comments")
    if comments == "":
        print("nulll")
    else:
        user_data = User_details.objects.get(auth_user=request.user)
        data = sub_space_comments.objects.create(sub_space_id_id=sub_space_id,
        added_by_id = user_data.id,user_auth_id_id =request.user.id ,comments = comments)

    return JsonResponse({"message":"success"},safe=False)



def get_task_comment(request):
    task_id = request.GET.get("task_id")
    comments = request.GET.get("comments")
    if comments == "":
        print("nulll")
    else:
        user_data = User_details.objects.get(auth_user=request.user)
        data = Add_task_comments.objects.create(add_task_id_id=task_id,
        added_by_id = user_data.id,user_auth_id_id =request.user.id ,comments = comments)

    return JsonResponse({"message":"success"},safe=False)



def generate_client_access_link(request):
    if request.method == "POST":
        access_id = request.POST.get("access_id")
        print("access_id::::::::::::",str(access_id))
        try:
            data = Project_user_access_link.objects.get(project_id_id=access_id)
        except:
            data1 = sub_space_master.objects.get(id=access_id)
            save_data = Project_user_access_link.objects.create(project_id_id=access_id,title=data1.sub_space_name)
            messages.success(request,str("success"))
            return redirect(request.META['HTTP_REFERER'])




def open_project(request,name):
    print("name:::::::::::::",str(name))
    data = Project_user_access_link.objects.get(slug=name)
    sub_space_data = sub_space_master.objects.get(id=data.project_id.id)
    space_id = sub_space_data.space_id
    task_data = Add_task_master.objects.filter(space_id = space_id,sub_space_id = sub_space_data.id,parent_id = None )

    task_details = list(task_data.values_list('id',flat=True))
    time_details = Task_time_details.objects.filter(task_id__in=task_details,user_auth_id = request.user)
    print("time_details:::::",time_details)
    total_hr = ""
    try : 
        total_price = sum(time_details.values_list('total_second', flat=True))
        total_hr = convert(total_price)
    except:
        pass

    context = {
        'sub_space_data':sub_space_data,
        'total_hr':total_hr,
        'time_details':time_details,
        "task_data":task_data
    }
    return render(request,'open_project.html',context)
    


def test_demo(request):
    return render(request,'test_demo.html')
   



#---------------------------------------------------------------------------------------------------chat module---------------------------------------------------------------



def chat(request):
    member_data = ""
    user_details_data = User_details.objects.get(auth_user = request.user)
    member_data = User_details.objects.filter(company_id =user_details_data.company_id).exclude(auth_user=request.user)

    context = {
        "member_data":member_data
    }
    return render(request, 'chat.html',context)


def chat_inner_page_action(request):

    id = request.GET.get("id")
    selected_user_data = User_details.objects.get(id=id)
    recev_id = User_details.objects.get(id=id)
    sender_auth_id = request.user.id
    receiver_auth_id = recev_id.auth_user.id
    room_no1 = "channelname"+str(receiver_auth_id)
    data_update_status = userMessage.objects.filter(send_user_id_id=receiver_auth_id,receiver_user_id_id=sender_auth_id,read_status=False).update(read_status=True)
    exists_data = User_chat_room.objects.filter(send_user_id_id=sender_auth_id,receiver_user_id_id=receiver_auth_id) or User_chat_room.objects.filter(send_user_id_id=receiver_auth_id,receiver_user_id_id=sender_auth_id)
    room_name = ''
    if exists_data:
        room_name = exists_data[0].room_name
        print("room_name:::",exists_data[0].room_name)
    else:
        room_name = 'chat_room'+str(sender_auth_id)+str(receiver_auth_id)
        data_save = User_chat_room.objects.create(send_user_id_id=sender_auth_id,receiver_user_id_id=receiver_auth_id,room_name=room_name)
    from django.db.models import F
    list1 = [sender_auth_id,receiver_auth_id]
    data_chat = userMessage.objects.filter(send_user_id_id__in=list1,receiver_user_id__in=list1).order_by(F('id').asc(nulls_last=True))
    # print("data_chat::::",str(data_chat))
    context = {
        'selected_user_data':selected_user_data,
        'room_name':room_name,
        'receiver_auth_id':receiver_auth_id,
        'data_chat':data_chat,
        'current_user_data':User_details.objects.get(auth_user=request.user),
        'room_no1':room_no1
    }
    return render(request,'chat_inner.html',context)

# Amar sir attachment update

def user_upload_chat_file_action(request):
    if request.method == "POST":
        chat_file = request.FILES['chat_file']
        send_user_id = request.POST.get("send_user_id")
        receiver_user_id = request.POST.get("receiver_user_id")
        import os
        extension = os.path.splitext(str(chat_file))[1]
        image_name = os.path.splitext(str(chat_file))[0]
       
        data_save = userMessage(read_status=False,send_user_id_id=send_user_id,receiver_user_id_id=receiver_user_id,message_type='file_type',image_extension=extension,image_name=image_name,file_path=chat_file)
        data_save.save()
        return JsonResponse({'message':'success'},safe=False)



# calendar updates

def calendar_detail(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    user_details_data = User_details.objects.get(auth_user = request.user)
    member_data = User_details.objects.filter(company_id =user_details_data.company_id)
    manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )

    status_name = status_name_master.objects.filter(company_id=user_details_data.company_id)

    space_master_data = ""
    sub_space_data =""
    space_dept = ""
    try:
        userdetails_data = User_details.objects.get(auth_user=request.user)

        # if user is company_admin (navab sir (all space of him))
        if userdetails_data.user_type == "company_admin":
            space_master_data = space_master.objects.filter(added_user_id=request.user)
            space_list = list(space_master_data.values_list('id',flat=True))
            space_dept = space_master.objects.get(id=space_list[0])
            sub_space_data = sub_space_master.objects.filter(space_id =space_list[0])
        else:
            # if user is company_user(their space only)
            sub_space = sub_space_master.objects.filter(invite_user_auth_id=request.user)
            user_permission_space = list(sub_space.values_list('space_id',flat=True))
            space_master_data = space_master.objects.filter(id__in=user_permission_space)

            space_list = list(space_master_data.values_list('id',flat=True))
            space_dept = space_master.objects.get(id=space_list[0])
            sub_space_data = sub_space_master.objects.filter(space_id =space_list[0])

    except:
        pass

    context = {
    "member_data" : member_data,
    "user_details_data":user_details_data,
    "status_name":status_name,
    "manager_data":manager_data,
    "space_master_data":space_master_data,
    "sub_space_data":sub_space_data,
    "space_dept":space_dept,
    "today_date":today_date
    }

    return render(request,"calendar_detail.html",context)


def get_group_details_calendar(request):
    today_date = datetime.today().strftime('%Y-%m-%d')
    space_id = request.GET.get("space_id")
    space_dept = space_master.objects.get(id=space_id)
    sub_space_data = sub_space_master.objects.filter(space_id=space_id)

    user_details_data = User_details.objects.get(auth_user=request.user)
    manager_data = User_details.objects.filter(user_level = "Manager",company_id = user_details_data.company_id.id )
    member_data = User_details.objects.filter(company_id =user_details_data.company_id)

    context = {
        "today_date":today_date,
        "sub_space_data":sub_space_data,
        "space_dept":space_dept,
        "manager_data":manager_data,
        "member_data":member_data
    }
    
    return render(request,'get_group_details_calendar.html',context)

   
def calendar_new(request):
    id = request.GET.get("type")
    sub_space_data = sub_space_master.objects.get(id=id)
    task_data = Add_task_master.objects.filter(sub_space_id_id=sub_space_data.id)
    sub_data = task_data.values_list('bucket_mapping_id', flat=True)
    sub_space_data_new = status_name_master.objects.filter(id__in=sub_data)
    return render(request,"calendar_new.html",{'sub_space_data':sub_space_data,'sub_space_data_new':sub_space_data_new})


from django.http import JsonResponse
def all_events(request):
    id = request.GET.get("type")
    sub_space_data = sub_space_master.objects.get(id=id)
    task_data = Add_task_master.objects.filter(sub_space_id_id=sub_space_data.id)
    out = []
    for event in task_data:
        from datetime import datetime
        df = datetime.fromisoformat(str(event.end_date))
        from datetime import timedelta
        date_time_obj = df + timedelta(days=1)
        date_to = date_time_obj.date()

        title_data = str(event.task_name) + " ( " + str(event.start_date) + " --> " + str(event.end_date) + " )"

        out.append({
            'title': title_data,
            'id': event.id,
            'start': event.start_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': date_to,
            'color': event.bucket_mapping_id.status_color,
        })
    return JsonResponse(out, safe=False)


def event_depended(request):
    from .models import progress, priority
    event_id = request.GET.get("event_id")
    task_data = Add_task_master.objects.get(id=event_id)
    bucket_data = status_name_master.objects.all()
    return render(request,"event_depended.html",{'task_data':task_data,'bucket_data':bucket_data,'progress':progress,'priority':priority})

def event_depended_action(request):
    task_id = request.POST.get("task_id")
    bucket = request.POST.get("bucket")
    progress = request.POST.get("progress")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    priority = request.POST.get("priority")
    data = Add_task_master.objects.get(id=task_id)
    if (str(data.bucket_mapping_id_id)==str(bucket)) and (data.progress==progress) and (data.priority==priority) and (str(data.start_date)==str(start_date)) and (str(data.end_date)==str(end_date)):
        messages.warning(request, str("No Updates"))
        return redirect(request.META['HTTP_REFERER'])
    else:
        task_data = Add_task_master.objects.filter(id=task_id).update(
            bucket_mapping_id_id=bucket,
            progress=progress,
            priority=priority,
            start_date=start_date,
            end_date=end_date,
        )
        messages.success(request, str("Updated Succesfully"))
        return redirect(request.META['HTTP_REFERER'])



def calendar_task(request):
    id = request.GET.get("type")
    sub_space_data_new = ""
    space_dept = ""
    try:
        userdetails_data = User_details.objects.get(auth_user=request.user)

        # if user is company_admin (navab sir (all space of him))
        if userdetails_data.user_type == "company_admin":
            space_dept = space_master.objects.get(id=id)
            sub_space_data = sub_space_master.objects.filter(space_id=space_dept)
            sub_data = sub_space_data.values_list('bucket_mapping_id', flat=True)
            sub_space_data_new = status_name_master.objects.filter(id__in=sub_data)
        else:
            # if user is company_user(their space only)
            space_dept = space_master.objects.get(id=id)
            sub_space_data = sub_space_master.objects.filter(space_id__in=space_dept)
            sub_data = sub_space_data.values_list('bucket_mapping_id', flat=True)
            sub_space_data_new = status_name_master.objects.filter(id__in=sub_data)

    except:
        pass
    return render(request, "calendar_task.html",{'sub_space_data_new':sub_space_data_new,'space_dept':space_dept})


def event_task(request):
    id = request.GET.get("type")
    sub_space_data = ""
    try:
        userdetails_data = User_details.objects.get(auth_user=request.user)

        # if user is company_admin (navab sir (all space of him))
        if userdetails_data.user_type == "company_admin":
            space_dept = space_master.objects.get(id=id)
            sub_space_data = sub_space_master.objects.filter(space_id=space_dept)
        else:
            # if user is company_user(their space only)
            space_dept = space_master.objects.get(id=id)
            sub_space_data = sub_space_master.objects.filter(space_id__in=space_dept)


    except:
        pass
    out = []
    for event in sub_space_data:
        from datetime import datetime
        df = datetime.fromisoformat(str(event.Actual_end_date))
        from datetime import timedelta
        date_time_obj = df + timedelta(days=1)
        date_to = date_time_obj.date()

        # title_data = str(event.task_name) + " ( " + str(event.start_date) + " --> " + str(date_to) + " )"

        out.append({
            'title': event.sub_space_name,
            'id': event.id,
            'start': event.Actual_start_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': date_to,
            'color': event.bucket_mapping_id.status_color,
        })
    return JsonResponse(out, safe=False)



def task_depended(request):
    from .models import progress, priority
    event_id = request.GET.get("event_id")
    task_data = sub_space_master.objects.get(id=event_id)
    bucket_data = status_name_master.objects.all()
    return render(request,"task_depended.html",{'task_data':task_data,'bucket_data':bucket_data,'progress':progress,'priority':priority})

def task_depended_action(request):
    task_data_id = request.POST.get("task_data_id")
    bucket = request.POST.get("bucket")
    progress = request.POST.get("progress")
    planning_start_date = request.POST.get("planning_start_date")
    planning_end_date = request.POST.get("planning_end_date")
    actual_start_date = request.POST.get("actual_start_date")
    actual_end_date = request.POST.get("actual_end_date")
    priority = request.POST.get("priority")
    data = sub_space_master.objects.get(id=task_data_id)
    if (str(data.bucket_mapping_id_id)==str(bucket)) and (data.progress==progress) and (data.priority==priority) and (str(data.Planning_start_date)==str(planning_start_date)) and (str(data.Planning_end_date)==str(planning_end_date)) and (str(data.Actual_start_date)==str(actual_start_date)) and (str(data.Actual_end_date)==str(actual_end_date)):
        messages.warning(request, str("No Updates"))
        return redirect(request.META['HTTP_REFERER'])
    else:
        task_data = sub_space_master.objects.filter(id=task_data_id).update(
            bucket_mapping_id_id=bucket,
            progress=progress,
            priority=priority,
            Planning_start_date=planning_start_date,
            Planning_end_date=planning_end_date,
            Actual_start_date=actual_start_date,
            Actual_end_date=actual_end_date,
        )
        messages.success(request, str("Updated Succesfully"))
        return redirect(request.META['HTTP_REFERER'])


def test_r1(request):
    if request.method == "POST":
        messages.success(request,"Successfully updated Project details")
        return redirect(request.META.get('HTTP_REFERER'))
        pass
    return render(request,'test_r1.html')