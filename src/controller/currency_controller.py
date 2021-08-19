"""
Segment Image Service
"""
from src.service.currency_service import CurrencyService
from src.util.decorator import token_required

from src.controller.router_config.router_config import ROUTER_CONFIG


class CurrencyController:
    """
    Account Controller
    """

    def __init__(self, app, req):
        """
        init
        :param app: object Flask
        :return:
        """
        self.currency_service = CurrencyService()
        self.getCurrency(app, req)
        self.addCurrency(app, req)
        self.updateCurrency(app, req)
        self.deleteCurrency(app, req)


    def getCurrency(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        print(ROUTER_CONFIG["api"]["v1"]["currency"]["path_list_currency"])

        currency_service = self.currency_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["currency"]["path_list_currency"]), methods=['GET'])
        @token_required
        def getCurrency():
            """
            add account of facebook
            """
            return currency_service.get()

    def addCurrency(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        print(ROUTER_CONFIG["api"]["v1"]["currency"]["path_add_currency"])

        currency_service = self.currency_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["currency"]["path_add_currency"]), methods=['POST'])
        # @token_required
        def addCurrency():
            """
            add account of facebook
            """
            return currency_service.post(req)

    def updateCurrency(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        print(ROUTER_CONFIG["api"]["v1"]["currency"]["path_update_currency"])

        currency_service = self.currency_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["currency"]["path_update_currency"]), methods=['PUT'])
        # @token_required
        def updateCurrency():
            """
            add account of facebook
            """
            return currency_service.put(req)

    def deleteCurrency(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        print(ROUTER_CONFIG["api"]["v1"]["currency"]["path_delete_currency"])

        currency_service = self.currency_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["currency"]["path_delete_currency"]), methods=['DELETE'])
        # @token_required
        def deleteCurrency():
            """
            add account of facebook
            """
            return currency_service.delete(req)
