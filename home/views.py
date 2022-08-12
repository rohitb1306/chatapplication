from django.shortcuts import render
from django.views.generic import TemplateView,ListView,View
from chat.models import Room
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
        room_public=Room.objects.filter(is_private=False,is_single_user=False)
        room_single=Room.objects.filter(is_single_user=True)
        lst=[]
        for i in room_single:
            if i.from_user==request.user.username or i.to_user==request.user.username:
                lst.append(i)
        paginator = Paginator(lst, 7) 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'home/index.html',{'page_obj':page_obj,'room_public':room_public})