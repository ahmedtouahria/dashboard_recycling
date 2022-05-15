import json
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from recycling.models import Contrat, Customer, MatierPremier, Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Min, Sum
from datetime import date, timedelta
from django.db.models.functions import TruncDay, TruncMonth
from django.core.serializers.json import DjangoJSONEncoder

@login_required(login_url="login")

def home(request):
    today_mony = Product.objects.aggregate(total_price=Sum('price'))
    today_profit = Product.objects.aggregate(total_price=Sum('price'))
    all_orders=Contrat.objects.filter(enterprise=request.user).count()
    new_order = Customer.objects.filter(
        created_at__day=date.today().day).count()
    quantity_stock_admin=MatierPremier.objects.aggregate(all_quantity=Sum('quantity'))
    new_clients = Customer.objects.filter(
        created_at__day=date.today().day).count()
    num_users = Customer.objects.all().count()
    num_orders = Customer.objects.all().count()
    num_products = Product.objects.all().count()
    # dashboard chart graphic
    chart_data = (
        Customer.objects.annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(y=Count("id"))
        .order_by("-date")
    )
    as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
    vendeurs = Customer.objects.filter(is_deche_vendeur=True)
    orders=Contrat.objects.filter(enterprise=request.user)
    context = {
        "vendeurs": vendeurs,
        "chart_data": as_json,
        "today_mony": today_mony,
        "today_profit": today_profit,
        "new_order": new_order,
        "new_clients": new_clients,
        "num_users": num_users,
        "num_partners": num_users,
        "num_orders": num_orders,
        "num_products": num_products,
        "orders":orders,
        "all_orders":all_orders,
        "quantity_stock_admin":quantity_stock_admin
    }
    return render(request, "pages/index.html", context)


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        type = request.POST["type"]
        address = request.POST["address"]
        
        if username and phone and password is not None:
            if username and phone and password != "":
                if type == "is_mp_client":
                    customer = Customer(
                        name=username, phone=phone, password=password, is_mp_client=True,address=address)
                    customer.save()
                elif type == "is_mp_client":
                    customer = Customer(
                        name=username, phone=phone, password=password, is_deche_vendeur=True,address=address)
                    customer.save()
                login(request, customer)
                return redirect("home")
            else:
                pass
        else:
            print("username and phone and password is  None")

    context = {}
    return render(request, "pages/sign_in.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            print(phone,password)
            try:
                user= Customer.objects.get(phone=phone,password=password)
            except Customer.DoesNotExist:
                user=None
            print(user)
            if user is not None:
                login(request, user)
                return redirect("home")

    context = {}
    return render(request, "pages/login.html", context)

@login_required(login_url="login")
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required(login_url="login")

def add(request):
    if request.user.is_mp_client:
        return redirect("home")
    else:
        if request.method == "POST":
            name = request.POST["name"]
            quantity = request.POST["quantity"]
            price = int(request.POST["price"])
            image = request.FILES.get("image")
            user = request.user
            print(user.is_deche_vendeur)
            if user.is_deche_vendeur:
                product = Product(user=user, name=name,
                              quantity=quantity, price=price, photo=image)
                product.save()
                messages.success(request, "Successfully added Product ")
            elif user.is_admin:
                mp = MatierPremier(user=user, name=name,
                               quantity=quantity, price=price, photo=image)
                mp.save()
                messages.success(request, "Successfully added MP ")
            else:
                messages.error(request, "Error ")
    context = {}
    return render(request, "pages/add.html", context)

@login_required(login_url="login")

def myproduct(request):
    user = request.user
    if user.is_deche_vendeur:
        products = Product.objects.filter(user=user)
    elif user.is_admin:
        products = MatierPremier.objects.filter(user=user)
        vendeurs = Customer.objects.filter(is_deche_vendeur=True)
    else:
        products = MatierPremier.objects.all()
        vendeurs=""
    context = {
        "products": products,
        "vendeurs": vendeurs,
    }
    return render(request, "pages/my_product.html", context)

@login_required(login_url="login")

def products(request, pk):
    user = request.user
    if user.admin:
        try:
            vendeur = Customer.objects.get(id=pk, is_deche_vendeur=True)
        except Customer.DoesNotExist:
            vendeur = None
        products = Product.objects.filter(user=vendeur)
    else:
        products = {}
    context = {
        "vendeur": vendeur,
        "products": products,

    }
    return render(request, "pages/products.html", context)

@login_required(login_url="login")

def edit_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except:
        product=None
    try:
        mp = MatierPremier.objects.get(id=pk)
    except:
        mp=None
    user = request.user
    if user.is_mp_client:
        return redirect("home")
    if request.method == "POST":
        name = request.POST["name"]
        quantity = request.POST["quantity"]
        price = request.POST["price"]
        image = request.FILES.get("image")
        if user.is_deche_vendeur:
            product.name = name
            product.quantity = quantity
            product.price = price
            product.image = image
            product.save()
            messages.success(request, "Successfully updated Product ")
        elif user.is_admin:
            mp.name = name
            mp.quantity = quantity
            mp.price = price
            mp.image = image
            mp.save()
            messages.success(request, "Successfully updated MP ")
        else:
            messages.error(request, "Error ")
    context = {"product": product,"mp":mp}
    return render(request, "pages/edit_product.html", context)
@login_required(login_url="login")
def mp_order(request,pk):
    mp=MatierPremier.objects.get(id=pk)
    entreprise=request.user
    if request.method=="POST":
        quantity=request.POST.get("quantity")
        total=mp.price*float(quantity)
        contrat=Contrat(enterprise=entreprise,matier=mp,quantity=quantity,total_price=total)
        contrat.save()
        return redirect("home")
    return render(request,"pages/demand_mp.html")