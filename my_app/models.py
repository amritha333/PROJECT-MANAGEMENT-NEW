from django.db import models
from django.contrib.auth.models import User

# Create your models here.


status_type = [
    ("To do","To do"),
    ("Completed","Completed"),
    ("Testing","Testing"),
     ("Onhold","Onhold"),

]

class task(models.Model):
    task_name = models.CharField(max_length=255,null=True)
    status = models.CharField(max_length=50,choices=status_type)


# Amritha Updates

class common_table(models.Model):
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_ownership",on_delete=models.CASCADE,null=True)
    created_dt = models.DateField(auto_now=True)
    updated_by =  models.ForeignKey(User, related_name="%(app_label)s_%(class)s_ownership1",on_delete=models.CASCADE,null=True)
    updated_dt = models.DateField(null=True)
    created_tm = models.TimeField(auto_now=True)
    updated_tm = models.TimeField(null=True)
    status = models.CharField(max_length=10, null=True)

    class Meta:
        abstract = True

class company_master(common_table):
    company_name = models.CharField(max_length=50,null=True)
    company_logo = models.FileField(upload_to="company_logo", null=True)
    tax_number = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=15, null=True)
    website = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    address = models.TextField(null=True)


password_generate_option = (
    ("Automatic","Automatic"),
    ("Manual","Manual"),
)

user_type = (
    ("company_admin","Company_admin"),
    ("company_user","Company_user")
)
user_level = (
    ("Manager","Manager"),
    ("Normal Staff","Normal Staff")
)

class User_details(common_table):
    auth_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_details_authuser", null=True)
    company_id = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name="user_details_company_id", null=True)
    company_name = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50,null=True)
    password_option =  models.CharField(max_length=50,choices=password_generate_option,null=True)
    password = models.CharField(max_length=50,null=True)
    user_type = models.CharField(max_length=20,choices=user_type,null=True)
    user_level = models.CharField(max_length=25,choices=user_level,null=True)
    photo = models.FileField(upload_to="user_image", null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    manager_auth = models.ForeignKey(User,on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_owner1",null=True)
   


class Role_master(common_table):
    auth_user = models.ForeignKey(User,related_name="role_auth_id",on_delete=models.CASCADE,null=True)
    role_name = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    company_id = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name="role_master_company_id", null=True)


navbar_name = (
    ("Company","Company"),
    ("User","User"),
    ("Role","Role"),
    ("Team member","Team member"),
    ("Tags","Tags"),
    ("Status","Status"),
)

class Role_mapping(common_table):
    role_master_id = models.ForeignKey(Role_master,related_name="Role_master_role_id",on_delete=models.CASCADE,null=True)
    navbar_name = models.CharField(max_length=50,choices=navbar_name,null=True)
    read = models.BooleanField(null=True)
    write = models.BooleanField(null=True)
    edit = models.BooleanField(null=True)
    delete = models.BooleanField(null=True)
    view_all = models.BooleanField(null=True)
    manage_all = models.BooleanField(null=True)

class user_permission_mapping(common_table):
    auth_user_id = models.ForeignKey(User,related_name="user_permision_auth",on_delete=models.CASCADE,null=True)
    user_id = models.ForeignKey(User_details,related_name="user_permision_userid",on_delete=models.CASCADE,null=True)
    role_mapping_id = models.ForeignKey(Role_master,related_name="user_permission_role_id",on_delete=models.CASCADE,null=True)
    start_dt = models.DateField(null=True)
    end_dt = models.DateField(null=True)
    description = models.TextField(null=True)


class user_active_account(common_table):
    user_id = models.ForeignKey(User_details,related_name="login_user_active_userid",on_delete=models.CASCADE,null=True)
    active_user_id = models.ForeignKey(User_details,related_name="user_active_userid",on_delete=models.CASCADE,null=True)
    active_auth_user_id = models.ForeignKey(User,related_name="active_auth_id",on_delete=models.CASCADE,null=True)


class status_name_master(common_table):
    active_user_id = models.ForeignKey(User_details,related_name="task_active_userid",on_delete=models.CASCADE,null=True)
    active_auth_user_id = models.ForeignKey(User,related_name="task_active_auth_id",on_delete=models.CASCADE,null=True)
    status_name = models.CharField(max_length=15,null=True)
    status_color = models.CharField(max_length=55,null=True)
    company_id = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name="status_company_id", null=True)

    def __str__(self) -> str:
        return self.status_name


class tags_name_master(common_table):
    active_user_id = models.ForeignKey(User_details,related_name="tags_active_userid",on_delete=models.CASCADE,null=True)
    active_auth_user_id = models.ForeignKey(User,related_name="tags_active_auth_id",on_delete=models.CASCADE,null=True)
    tags_name = models.CharField(max_length=15,null=True)
    tags_color = models.CharField(max_length=55,null=True)
    company_id = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name="tags_company_id", null=True)

    def __str__(self) -> str:
        return self.tags_name

class space_master(common_table):
    space_name = models.CharField(max_length=50,null=True)
    task_status = models.ManyToManyField(status_name_master)
    active_account_id = models.ForeignKey(User_details,related_name="space_active_userid",on_delete=models.CASCADE,null=True)
    added_user_id = models.ForeignKey(User,related_name="space_auth_id",on_delete=models.CASCADE,null=True)



buckets = (
    ("todo","To do"),
    ("completed","Completed"),
    ("testing","Testing"),
    ("onhold","On Hold")
)

progress = (
    ("Not Started","Not Started"),
    ("In progress","In progress"),
    ("Completed","Completed"),
)
priority = (
    ("Urgent","Urgent"),
    ("Important","Important"),
    ("Medium","Medium"),
    ("Low","Low")
)

class sub_space_master(common_table):
    space_id = models.ForeignKey(space_master,related_name="sub_space_master_id",on_delete=models.CASCADE,null=True)
    sub_space_name = models.CharField(max_length=50,null=True)
    active_account_id = models.ForeignKey(User_details,related_name="sup_space_master_userid",on_delete=models.CASCADE,null=True)
    added_user_id = models.ForeignKey(User,related_name="sub_space_master_auth_id",on_delete=models.CASCADE,null=True)
    bucket_mapping_id = models.ForeignKey(status_name_master,related_name="sub_space_bucket_id",on_delete=models.CASCADE,null=True)
    progress = models.CharField(max_length=50,choices=progress,null=True)
    priority = models.CharField(max_length=50,choices=priority,null=True)
    notes = models.TextField(null=True)
    Planning_start_date = models.DateField(blank=True)
    Planning_end_date = models.DateField(blank=True)
    Actual_start_date = models.DateField(blank=True)
    Actual_end_date= models.DateField(blank=True)
    invite_user_details_id = models.ManyToManyField(User_details,related_name="sub_space_userdetails")
    invite_user_auth_id = models.ManyToManyField(User,related_name="sub_space_auth")
    sub_space_manager = models.ForeignKey(User,related_name="sub_space_master_manager",on_delete=models.CASCADE,null=True)
    tag_id = models.ManyToManyField(tags_name_master,related_name="sub_space_tag")

class sub_space_checklist(common_table):
    sub_space_id = models.ForeignKey(sub_space_master,related_name="sub_space_checklist",on_delete=models.CASCADE,null=True)
    milestone = models.CharField(max_length=50,null=True)
    due_date = models.DateField(blank=True,null=True)

class sub_space_attachment(common_table):
    sub_space_id = models.ForeignKey(sub_space_master,related_name="sub_space_attachment",on_delete=models.CASCADE,null=True)
    file_name = models.CharField(max_length=50,null=True)
    file_type = models.CharField(max_length=30,null=True)
    attached_file = models.FileField(upload_to="sub_space_attachment", null=True)
    text_content = models.CharField(max_length=200,null=True)
    added_by = models.ForeignKey(User,related_name="sub_space_auth_id",on_delete=models.CASCADE,null=True)

class sub_space_comments(common_table):
    sub_space_id = models.ForeignKey(sub_space_master,related_name="sub_space_comments",on_delete=models.CASCADE,null=True)
    added_by = models.ForeignKey(User_details,related_name="sub_space_comment_user",on_delete=models.CASCADE,null=True)
    user_auth_id = models.ForeignKey(User,related_name="sub_space_comment_auth",on_delete=models.CASCADE,null=True)
    comments=  models.TextField(null=True)

class Add_task_master(common_table):
    space_id = models.ForeignKey(space_master,related_name="add_task_master_space",on_delete=models.CASCADE,null=True)
    sub_space_id = models.ForeignKey(sub_space_master,related_name="add_sub_space",on_delete=models.CASCADE,null=True)
    parent_id = models.ForeignKey('self',blank=True,null=True,related_name='sub_task',on_delete=models.CASCADE)
    task_name = models.CharField(max_length=50,null=True)
    buckets = models.CharField(max_length=50,choices=buckets,null=True)
    bucket_mapping_id = models.ForeignKey(status_name_master,related_name="Add_task_master_bucket_id",on_delete=models.CASCADE)
    progress = models.CharField(max_length=50,choices=progress,null=True)
    priority = models.CharField(max_length=50,choices=priority,null=True)
    notes = models.TextField(null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    task_status = models.CharField(max_length=50,null=True)
    tag_id = models.ManyToManyField(tags_name_master,related_name="Add_task_master_tag")
    invite_user_details_id = models.ManyToManyField(User_details,related_name="add_task_user_id")
    invite_user_auth_id = models.ManyToManyField(User,related_name="add_task_auth_id")
    multiple_parent_id = models.ManyToManyField('Add_task_master', blank=True,related_name="Add_task_master_parent_many_to_many")


class Add_task_checklist(common_table):
    add_task_id = models.ForeignKey(Add_task_master,related_name="add_task_checklist",on_delete=models.CASCADE,null=True)
    item_name = models.CharField(max_length=50,null=True)
    due_date = models.DateField(blank=True,null=True)

class Add_task_attachment(common_table):
    add_task_id = models.ForeignKey(Add_task_master,related_name="add_attachment",on_delete=models.CASCADE,null=True)
    file_name = models.CharField(max_length=50,null=True)
    file_type = models.CharField(max_length=30,null=True)
    attached_file = models.FileField(upload_to="task_attachment", null=True)  
    text_content = models.CharField(max_length=200,null=True)
    added_by = models.ForeignKey(User,related_name="task_auth_id",on_delete=models.CASCADE,null=True)

class Add_task_comments(common_table):
    add_task_id = models.ForeignKey(Add_task_master,related_name="task_comments",on_delete=models.CASCADE,null=True)
    added_by = models.ForeignKey(User_details,related_name="task_comment_user",on_delete=models.CASCADE,null=True)
    user_auth_id = models.ForeignKey(User,related_name="task_comment_auth",on_delete=models.CASCADE,null=True)
    comments=  models.TextField(null=True)




class Add_meeting(common_table):
    invite_user_id = models.ManyToManyField(User_details,related_name="Create_meeting_user_id")
    Title = models.CharField(max_length=22,null=True)
    meeting_dt = models.DateField()
    meeting_start_tm = models.TimeField()
    meeting_end_tm = models.TimeField()
    channel_name = models.CharField(max_length=255)
    Description = models.TextField(null=True)
    completed_status = models.CharField(max_length=25,null=True)


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User_chat_room(models.Model):
    send_user_id = models.ForeignKey(User,related_name='User_chat_room_send_user_id',on_delete=models.CASCADE,null=True)
    receiver_user_id = models.ForeignKey(User,related_name='User_chat_room_receiver_user_id',on_delete=models.CASCADE,null=True)
    room_name = models.SlugField(unique=True)



messageType =(
    ("text","text"),
    ('file_type','file_type')
)


class userMessage(models.Model):
    send_user_id = models.ForeignKey(User,related_name='userMessage_send_user_id',on_delete=models.CASCADE,null=True)
    receiver_user_id = models.ForeignKey(User,related_name='userMessage_receiver_user_id',on_delete=models.CASCADE,null=True)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(null=True)
    message_type = models.CharField(choices=messageType,null=True,max_length=25)
    image_name = models.CharField(max_length=25,null=True)
    image_extension = models.CharField(max_length=25,null=True)
    file_path = models.FileField(upload_to='chat_attachment',null=True)
    
    
notification_type_data = (
    ("late_task","late_task"),
)
notification_category = (
    ("subspace","subspace"),
    ("subtask","subtask"),
)

class Notification(models.Model):
    notification_type = models.CharField(max_length=255,null=True,choices=notification_type_data)
    message = models.TextField(null=True)
    auth_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notification_auth_user", null=True)
    due_date = models.DateField(null=True)
    task_name = models.CharField(max_length=100,null=True)
    task_category = models.CharField(max_length=50,null=True,choices=notification_category)


# stopwatch table

class Task_time_details(models.Model):
    starting_time = models.TimeField(null=True)
    current_date = models.DateField(null=True)
    counter = models.TimeField(null=True)
    timefield_counter = models.DateTimeField(null=True)
    total_second = models.IntegerField(null=True)
    task_id = models.ForeignKey(Add_task_master,related_name="task_time_task_id",on_delete=models.CASCADE,null=True)
    user_auth_id = models.ForeignKey(User,related_name="task_time_auth_user",on_delete=models.CASCADE,null=True)
    user_details_id = models.ForeignKey(User_details,related_name="task_time_userid",on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=30,null=True)
    button_status = models.CharField(max_length=30,null=True)
    end_status = models.CharField(max_length=30,null=True)


class History_task_time(models.Model):
    task_time_id = models.ForeignKey(Task_time_details,related_name="history_task_time_id",on_delete=models.CASCADE,null=True)
    starting_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    counter = models.TimeField(null=True)
    task_id = models.ForeignKey(Add_task_master,related_name="history_time_task_id",on_delete=models.CASCADE,null=True)
    user_auth_id = models.ForeignKey(User,related_name="history_time_auth_user",on_delete=models.CASCADE,null=True)

class Sub_space_time_details(models.Model):
    starting_time = models.TimeField(null=True)
    current_date = models.DateField(null=True)
    counter = models.TimeField(null=True)
    sub_space_id = models.ForeignKey(sub_space_master,related_name="sub_space_task_id",on_delete=models.CASCADE,null=True)
    user_auth_id = models.ForeignKey(User,related_name="sub_space_time_auth_user",on_delete=models.CASCADE,null=True)
    user_details_id = models.ForeignKey(User_details,related_name="sub_space_time_userid",on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=30,null=True)
    button_status = models.CharField(max_length=30,null=True)


class History_sub_space_time(models.Model):
    task_time_id = models.ForeignKey(Sub_space_time_details,related_name="history_sub_space_time_id",on_delete=models.CASCADE,null=True)
    starting_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    counter = models.TimeField(null=True)
    sub_space_id = models.ForeignKey(sub_space_master,related_name="history_time_sub_space_id",on_delete=models.CASCADE,null=True)
    user_auth_id = models.ForeignKey(User,related_name="history_sub_space_auth_user",on_delete=models.CASCADE,null=True)



from django.utils.text import slugify
class Project_user_access_link(models.Model):
    project_id =  models.OneToOneField(sub_space_master,related_name="Project_user_access_link_project_id",on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    def save(self, *args, **kwargs):        
        if not self.slug:            
            self.slug = slugify(rand_slug_model() + "-" + self.title)        
        super(Project_user_access_link, self).save(*args, **kwargs)

import string
import random
def rand_slug_model():    
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(1))
