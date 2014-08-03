from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("",

    url(r"^admin/", include(admin.site.urls)),

    # Clone related urls.
    url(r"^$", "clone.views.index", name="index"),
    url(r"^register/", "clone.views.register", name="register"),
    url(r"^login/", "clone.views.login_user", name="login"),
    url(r"^logout/", "clone.views.logout_user", name="logout"),
    url(r"^home/", "clone.views.home", name="home"),
    url(r"^new_product/", "clone.views.new_product", name="new_product"),
    url(r"^products/", "clone.views.products", name="products"),
    url(r"^payment_success", "clone.views.payment_success", name="payment_success"),

)
