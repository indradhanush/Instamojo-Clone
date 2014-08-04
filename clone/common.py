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
