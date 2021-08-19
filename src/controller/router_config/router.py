"""
module Router for endpoint
"""
from src.controller.currency_controller import CurrencyController
from src.controller.user_controller import UserController
from src.controller.transaction_controller import TransactionController
from src.controller.auth_controller import AuthController

class Router:
    """
     init route for all resource
     @param {*} app
    """

    def __init__(self, app, request):
        self.user_controller = UserController(app, request)
        self.transaction_controller = TransactionController(app, request)
        self.auth_controller = AuthController(app, request)
        self.currency_controller = CurrencyController(app, request)