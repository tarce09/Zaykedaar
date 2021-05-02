from django.shortcuts import render,redirect
from django.views import View
from .models import MenuItem,Category,OrderModel
from django.conf import settings
# Create your views here.

class Index(View):
    def get(self,request,*args, **kwargs):
        return render(request,'customer/index.html')

class About(View):
    def get(self,request,*args, **kwargs):
        return render(request,'customer/about.html')

class Order(View):       
          

    def get(self,request,*args, **kwargs):
        appetizers=MenuItem.objects.filter(category__name__contains='Apetizer')
        main=MenuItem.objects.filter(category__name__contains='Main')
        derserts=MenuItem.objects.filter(category__name__contains='Desert')
        drinks=MenuItem.objects.filter(category__name__contains='Drink')
        
        context={
            'appetizers':appetizers,
            'main':main,
            'derserts':derserts,
            'drinks':drinks,
        }

        return render(request,'customer/order.html',context)

    
    def post(self,request,*args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip')


        order_items={
            'items':[],
        }
        items=request.POST.getlist("items[]")

        for item in items:
            num=int(item)
            menu_item=MenuItem.objects.get(pk__contains=int(num))
            item_data={
                'id':menu_item.pk,
                'name':menu_item.name,
                'price':menu_item.price,
            }


            order_items['items'].append(item_data)
        price=0
        item_ids=[]

        for item in order_items['items']:
            price+=item['price']
            item_ids.append(item['id'])

        order=OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,)

        order.items.add(*item_ids)

        context={
            'items':order_items['items'],
            'price':price,
            'key': settings.PUBLISHABLE_KEY
        }

        return render(request,'customer/order_confirmation.html',context)
        


        