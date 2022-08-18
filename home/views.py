from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,View
from chat.models import Room, Room_users
from django.core.paginator import Paginator
# Create your views here.
# class Index(ListView):
#     template_name='home/index.html'
#     model=Room
#     paginate_by=10
#     paginate_orphans=1

#     def get_queryset(self):
#         return Room.objects.filter(is_private=False,is_single_user=False)

class Index(View):
    def get(self,request):
        if request.user.is_authenticated:
            room_public=Room.objects.filter(is_private_group=False,is_single_user=False)
            room_single=Room.objects.filter(is_single_user=True)
            room_group_private=Room.objects.filter(is_private_group=True)

            lst1=[]
            for i in room_group_private:
                if Room_users.objects.filter(room=i,user=request.user):
                    lst1.append(i)
            
            lst,lst2=[],{}
            for i in room_single:
                if Room_users.objects.filter(room=i,user=request.user):
                    all_users_inroom=Room_users.objects.filter(room=i)
                    lst.append(i)
                    lst2[i]=all_users_inroom
            paginator = Paginator(lst, 7) 

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request,'home/index.html',{'page_obj':page_obj,'room_public':room_public,'private_group':lst1,"all_user_inroom":lst2})
        else:
            return redirect('login')