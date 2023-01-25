from django import template

from my_app.models import userMessage
register = template.Library()

@register.filter(name='get_chat_count')
def get_chat_count(value,args):
    print("----------start get chat count----------------")
    print(value)
    print(args)
    print("-----------end get chat count----------------")
    data_count = userMessage.objects.filter(send_user_id_id=args,receiver_user_id_id=value,read_status=False).count()
    return data_count