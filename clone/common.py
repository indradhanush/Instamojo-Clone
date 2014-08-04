"""
Common variables and utilities.
"""

# System imports
import os


# Reply messages.
REGISTER_SUCCESS = "Thank you for registering."
REGISTER_FAIL = "Seems like an account is already registered by that email."

LOGIN_SUCCESS = "You have now logged in."
LOGIN_FAIL = "Wrong username/password combination."
LOGOUT_SUCCESS = "You have been logged out."

USER_NOT_ACTIVE = "You account has been disabled. Contact the admin."


# Context keys
USERNAME_KEY = "username"

TITLE_KEY = "title"
DESCRIPTION_KEY = "description"
PRICE_KEY = "base_price"
CURRENCY_KEY = "currency"
REDIRECT_URL_KEY = "redirect_url"

ADDED_BY_KEY = "added_by"
DATE_ADDED_KEY = "date_added"
URL_KEY = "url"

PRODUCT_ADD_SUCCESS = "The product was added successfully."
PRODUCT_BUY_SUCCESS = "Congratulations! You bought the product!"
PRODUCT_BUY_FAIL = "Sorry. Something went wrong with that payment."

INSTAMOJO_BASE_URL = "https://www.instamojo.com/api/1.1/"

def create_headers():
    """
    Simple wrapper to create auth headers.

    :return: Authentication Headers.
    :rtype: dict
    """
    return {
        "X-Api-Key": os.environ["INSTAMOJO_KEY"],
        "X-Auth-Token": os.environ["INSTAMOJO_SECRET"]
    }
