from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils.timezone import datetime
from customer.models import OrderModel

class DashBoard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self,request,*args,**kwargs):
        today=datetime.today()
        orders=OrderModel.objects.filter(createdOn__year=today.year,createdOn__month=today.month,createdOn__day=today.day)
        total_revenue=0
        for order in orders:
            total_revenue+=order.price
        context={
            'orders':orders,
            'total_revenue':total_revenue,
            'total_orders':len(orders)
        }

        return render(request,"restaurant/dashboard.html",context)

    def test_func(self):
        return self.request.user.groups.filter(name="staff").exists()