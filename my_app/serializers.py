from rest_framework import serializers
from .models import status_name_master,Add_task_master,Add_task_access_user,sub_space_master


class sub_space_master_Serializer(serializers.ModelSerializer):
    my_assign_user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = sub_space_master
        fields  = ['id','space_id','sub_space_name','priority','progress','end_date','invite_user_details_id'] 
    def get_my_assign_user(self,obj):
        data = Add_task_access_user.objects.filter(add_task_id=obj.id).values('id','invite_user_details_id__name')
        return data

class status_name_master_Serailzer(serializers.ModelSerializer):
    mapping_obj = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = status_name_master
        fields  = ['id','status_name','status_color','mapping_obj'] 
        
    def get_mapping_obj(self,obj):
        space_id = self.context.get("space_id")
        data = sub_space_master.objects.filter(space_id=space_id,bucket_mapping_id=obj.id)
        print("data:",data)
        return data





