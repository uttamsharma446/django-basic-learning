from dataclasses import fields
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import accounts
from .models import *
from .forms import CustomerForm, OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm(request.POST)
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'customer': customer,
               'total_orders': total_orders,
               'pending_orders': pending_orders,
               'delivered_orders': delivered_orders

               }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def customer(request, customerId):
    customer = Customer.objects.get(id=customerId)
    order = customer.order_set.all()
    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs
    order_count = order.count()
    context = {'customer': customer,
               'order': order, 'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})


@login_required(login_url='login')
def createOrder(request, custId):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=custId)

    # form = OrderForm(initial={'customer': customer})
    formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    context = {'formSet': formSet}
    if request.method == "POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        print(formset.is_valid())
        # if formset.is_valid():
        formset.save()
        return redirect('/')
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, orderId):
    order = Order.objects.get(id=orderId)
    form = OrderForm(instance=order)
    context = {'form': form}
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, orderId):
    order = Order.objects.get(id=orderId)
    context = {'order': order}
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='login')
def updateCustomer(request, custId):
    customer = Customer.objects.get(id=custId)
    form = CustomerForm(instance=customer)
    context = {'form': form}
    if (request.method == "POST"):
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customer/'+str(customer.id))
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
def deleteCustomer(request, custId):
    customer = Customer.objects.get(id=custId)
    context = {'customer': customer}
    if request.method == 'POST':
        customer.delete()
        return redirect('/')
    return render(request, 'accounts/delete_customer.html', context)


@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm()
    context = {'form': form}
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/customer_form.html', context)
