"""
Views for the app clone.
"""

# Third party imports
import requests
try:
    import simplejson as json
except ImportError:
    import json

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
    USERNAME_KEY,
    PRODUCT_ADD_SUCCESS,
    PRODUCT_BUY_SUCCESS,
    PRODUCT_BUY_FAIL,
    INSTAMOJO_BASE_URL,
    TITLE_KEY,
    DESCRIPTION_KEY,
    PRICE_KEY,
    CURRENCY_KEY,
    REDIRECT_URL_KEY,
    ADDED_BY_KEY,
    DATE_ADDED_KEY,
    URL_KEY,
    create_headers
)
from clone.models import Product
from instamojo_clone.settings import REDIRECTION_URL


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
    """
    Default view for a logged in user.
    """
    context = {}
    user = request.user
    context[USERNAME_KEY] = user.first_name or user.username
    return render(request, "clone/home.html", context)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def new_product(request):
    """
    View to handle requests for adding a new product.
    """
    payload = {}
    payload[TITLE_KEY] = request.POST.get(TITLE_KEY, "")
    payload[DESCRIPTION_KEY] = request.POST.get(DESCRIPTION_KEY, "")
    payload[PRICE_KEY] = request.POST.get("price", "")
    payload[CURRENCY_KEY] = request.POST.get(CURRENCY_KEY, "")
    payload[REDIRECT_URL_KEY] = REDIRECTION_URL

    headers = create_headers()
    endpoint = "{0}links/".format(INSTAMOJO_BASE_URL)
    response = requests.post(endpoint, headers=headers, data=payload)
    response_body = json.loads(response.text)

    product = Product(username=request.user, title=payload[TITLE_KEY],
                      description=payload[DESCRIPTION_KEY],
                      currency=payload[CURRENCY_KEY],
                      base_price=payload[PRICE_KEY],
                      url=response_body["link"]["url"]
                  )
    product.save()
    messages.add_message(request, messages.SUCCESS, PRODUCT_ADD_SUCCESS)
    return redirect("/home/")


@login_required
def products(request):
    """
    View to list all the products on the site.
    """
    products_list = Product.objects.filter(sold=False).order_by("-date_added")
    all_products = []
    for prod in products_list:
        product_detail = {}
        product_detail[ADDED_BY_KEY] = prod.username.username
        product_detail[TITLE_KEY] = prod.title
        product_detail[DESCRIPTION_KEY] = prod.description
        product_detail["price"] = prod.base_price
        product_detail[CURRENCY_KEY] = prod.currency
        product_detail[DATE_ADDED_KEY] = prod.date_added
        product_detail[URL_KEY] = prod.url

        all_products.append(product_detail)

    context = {"products": all_products}
    return render(request, "clone/products.html", context)


@login_required
@require_http_methods(["GET"])
def payment_success(request):
    """
    View to handle redirects after a product is bought on the instamojo
    website.
    """
    context = {}
    payment_id = request.GET.get("payment_id", "")
    if payment_id:
        # Redirected here after a checkout.
        endpoint = "{0}payments/{1}".format(INSTAMOJO_BASE_URL, payment_id)
        headers = create_headers()
        response = requests.get(endpoint, headers=headers)
        payment_info = json.loads(response.text)
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
