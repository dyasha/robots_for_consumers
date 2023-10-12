from django.shortcuts import render

from customers.models import Customer
from robots.models import Robot
from waitlist.models import WaitList

from .forms import OrderForm
from .models import Order


class OrderCreate:
    @staticmethod
    def read_data(customer_email, serial):
        """Выборка данных из БД"""
        customer = Customer.objects.get_or_create(email=customer_email)
        count_robots = Robot.objects.filter(serial=serial).count()
        count_orders = Order.objects.filter(robot_serial=serial).count()
        result = count_robots - count_orders
        return customer, result

    @staticmethod
    def create_waitlist(customer, robot_serial):
        """Создание объекта листа ожидания."""
        WaitList.objects.get_or_create(
            customer=customer, robot_serial=robot_serial
        )

    @staticmethod
    def create_order(request):
        "Создание заказа."
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                customer_email = form.cleaned_data["customer_email"]
                serial = form.cleaned_data["serial"]
                customer, result = OrderCreate.read_data(
                    customer_email, serial
                )
                if result > 0:
                    order = Order(customer=customer[0], robot_serial=serial)
                    order.save()
                    return render(request, "orders/complete_order.html")
                else:
                    OrderCreate.create_waitlist(customer[0], serial)
                    return render(request, "orders/waiting_list.html")
        else:
            form = OrderForm()

        return render(request, "orders/create_order.html", {"form": form})
