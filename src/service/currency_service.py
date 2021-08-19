"""
Account service
"""
import json


from src.models import TransactionModel, UserModel, CurrencyModel


class CurrencyService:
    """
    Account service
    """

    def __init__(self):
        self.currency_model = CurrencyModel()

    def get(self):
        currency = self.currency_model.find_all()
        list_currency = []
        for item in currency:
            data = {
                "id": item.id,
                "code": item.code,
                "description": item.description
            }
            list_currency.append(data)
            return {"result": list_currency}
        return {'message': 'Currency not found'}, 404

    def post(self, req):
        data = json.loads(req.data)
        if self.currency_model.find_by_code(data['code']):
            return {'message': "A currency with name '{}' already exists.".format(data['code'])}, 400

        result, err = self.currency_model.add_currency(data)
        if err:
            return {"message": "An error occurred creating the currency."}, 500
        return {"message": "Add currency success"}, 200

    def put(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        currency = self.currency_model.find_by_id(data['id'])
        if currency:
            if not self.currency_model.find_by_code(data['code']):
                result, err = self.currency_model.update_currency(currency, data)
                if err:
                    return {"message": "An error occurred update the store."}, 500
                return {"message": "Update currency success"}, 200
        return {'message': "A currency with code '{}' already exists.".format(data['code'])}, 400

    def delete(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        currency = self.currency_model.find_by_id(data['id'])
        if currency:
            result, err = self.currency_model.delete_currency(currency)
            if err:
                return {"message": "An error occurred delete the store."}, 500
            return {"message": "Delete currency success"}, 200
        return {'message': "A currency with code '{}' not exists.".format(data['code'])}, 400

