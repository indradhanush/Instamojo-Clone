# System imports
import os

# Django imports
from django.shortcuts import (
    render,
    redirect
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Local imports
from clone.common import (
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT_SUCCESS,
    USER_NOT_ACTIVE,
    REPLY_KEY,
    USERNAME_KEY,
    PRODUCT_ADD_SUCCESS,
    PRODUCT_BUY_SUCCESS,
    PRODUCT_BUY_FAIL
)
from clone.models import Product
from instamojo_clone.settings import REDIRECTION_URL

# Instamojo API imports
from instamojo import Instamojo


def prepare_api_request():
    return Instamojo(api_key=os.environ["INSTAMOJO_KEY"],
                     auth_token=os.environ["INSTAMOJO_SECRET"])


@require_http_methods(["GET", "POST"])
def index(request):
    """
    Default landing page.
    """
    if request.user.is_authenticated():
        return redirect("clone.views.home")

    return render(request, "clone/index.html")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def register(request):
    """
    View for handling register requests.
    """
    if request.method == "GET":
        return redirect("clone.views.index")
    elif request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = User(username=username, email=username)
            user.set_password(password)
            # user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, REGISTER_SUCCESS)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("clone.views.home")
        else:
            messages.add_message(request, messages.ERROR, REGISTER_FAIL)
            return redirect("clone.views.index")


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """
    View to handle login requests.
    """
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, LOGIN_SUCCESS)
            redirect_to = "clone.views.home"
        else:
            messages.add_message(request, messages.ERROR, USER_NOT_ACTIVE)
            redirect_to = "clone.views.index"
    else:
        messages.add_message(request, messages.ERROR, LOGIN_FAIL)
        redirect_to = "clone.views.index"
    return redirect(redirect_to)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def logout_user(request):
    """
    View to handle logout requests.
    """
    logout(request)
    messages.add_message(request, messages.SUCCESS, LOGOUT_SUCCESS)
    return redirect("clone.views.index")


@login_required
@require_http_methods(["GET", "POST"])
def home(request):
    context = {}
    user = request.user
    context[USERNAME_KEY] = user.first_name or user.username
    return render(request, "clone/home.html", context)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def new_product(request):
    title = request.POST.get("title", "")
    description = request.POST.get("description", "")
    price = request.POST.get("price", "")
    currency = request.POST.get("currency", "")
    api = Instamojo(api_key=os.environ["INSTAMOJO_KEY"],
                    auth_token=os.environ["INSTAMOJO_SECRET"])
    response = api.link_create(title=title, description=description,
                               base_price=price, currency=currency,
                               redirect_url=REDIRECTION_URL)

    product = Product(username=request.user, title=title,
                      description=description, currency=currency,
                      base_price=price, url=response["link"]["url"],
    )
    product.save()
    messages.add_message(request, messages.SUCCESS, PRODUCT_ADD_SUCCESS)
    return redirect("/home/")


def products(request):
    products_list = Product.objects.filter(sold=False)
    all_products = []
    for prod in products_list:
        product_detail = {}
        product_detail["added_by"] = prod.username.username
        product_detail["title"] = prod.title
        product_detail["description"] = prod.description
        product_detail["price"] = prod.base_price
        product_detail["currency"] = prod.currency
        product_detail["date_added"] = prod.date_added
        product_detail["url"] = prod.url

        all_products.append(product_detail)

    context = {"products": all_products}
    return render(request, "clone/products.html", context)


@login_required
@require_http_methods(["GET"])
def payment_success(request):
    context = {}
    payment_id = request.GET.get("payment_id", "")
    if payment_id:
        # Redirected here after a checkout.
        api = prepare_api_request()
        payment_info = api.payment_detail(payment_id)
        payment = payment_info["payment"]
        filter_list = []

        for key, value in payment.items():
            if payment.get(key):
                filter_list.append((key, value))

        context["payment"] = filter_list
        if payment_info["success"]:
            message_level = messages.SUCCESS
            msg = PRODUCT_BUY_SUCCESS
        else:
            message_level = messages.ERROR
            msg = PRODUCT_BUY_FAIL

        messages.add_message(request, message_level, msg)

    return render(request, "clone/success.html",  context)
