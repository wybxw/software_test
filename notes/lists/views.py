from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item,List
def new_list(request):
    list_user = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list=list_user)
    return redirect(f'/lists/{list_user.id}/')
def view_list(request,list_id):
    list_user = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_id)
    return render(request,'list.html', {'items': items})

def home_page(request):
    # if request.method == 'POST':
        # return HttpResponse(request.POST['item_text'])
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-new-page/')
    # else:
        # new_item_text = ''
    # item = Item()
    # item.text = request.POST.get('item_text','')
    # item.save()
    # items = Item.objects.all()
    return render(request,'home.html')
# Create your views here.
