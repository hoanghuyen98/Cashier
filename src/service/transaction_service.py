"""
Account service
"""
import json
from datetime import datetime
from http import HTTPStatus

import jwt


from config import key
from src.models import TransactionModel, UserModel, CurrencyModel


class TransactionService:
    """
    Account service
    """

    def __init__(self):
        self.transaction_model = TransactionModel()
        self.user_model = UserModel()

    def get(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        try:
            payload = jwt.decode(req.headers.get('Authorization'), key)
            transactions = self.transaction_model.find_by_user_id(payload['sub'])
            result = []
            for transaction in transactions:
                trans = {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "content": transaction.content,
                    "user_id": transaction.user_id,
                    "created_at": transaction.created_at,
                    "updated_at": transaction.updated_at,
                    "currency_id": transaction.currency_id,
                    "action_type": transaction.action_type.value
                }
                result.append(trans)

            return {"result": result}
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Authorization: {}'.format(ex)
            }
            return response_object, 409

    def add(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        balance = 0
        payload = jwt.decode(req.headers.get('Authorization'), key)
        user = UserModel.query.filter_by(id=payload['sub']).first()
        currency = CurrencyModel.query.filter_by(id=data['currency_id']).first()
        data['user_id'] = user.id
        if user:
            latest_transaction = self.transaction_model.find_by_latest_transaction(data)
            if latest_transaction:
                balance = latest_transaction.balance
                print("balance: ", latest_transaction.balance)
                print("id: ", latest_transaction.id)

            if data['action_type'] == 'withdrawals':
                if balance < data['amount']:
                    response_object = {
                        'status': 'fail',
                        'message': "users don't have enough money"
                    }
                    return response_object, 409
                else:
                    balance = balance - data['amount']

            elif data['action_type'] == 'deposits':
                balance = balance + data['amount']
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Action only include: deposits, withdrawals'
                }
                return response_object, 409

            data['user_id'] = payload['sub']
            data['balance'] = balance
            result = self.transaction_model.add_transaction(data, user)
            return result
            # pass
        response_object = {
            'status': "fail",
            'message': 'User not found'
        }
        return response_object, 409

    def put(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        try:
            payload = jwt.decode(req.headers.get('Authorization'), key)
            transaction = self.transaction_model.find_by_id_and_name(data["id"], payload['sub'])
            if transaction:
                result, err = self.transaction_model.update_transaction(transaction, data)
                if err:
                    return err
                return result
            return "fails"
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Authorization: {}'.format(ex)
            }
            return response_object, 409

    # def delete(self, req):
    #
    #     """
    #     add account of facebook
    #     :param req: object
    #     :return:
    #     """
    #     data = json.loads(req.data)
    #     try:
    #         payload = jwt.decode(req.headers.get('Authorization'), key)
    #         transaction = self.transaction_model.find_by_id_and_name(data["id"], payload['sub'])
    #         if transaction:
    #             result, err = self.transaction_model.delete_transaction(transaction)
    #             if err:
    #                 return err
    #             return result
    #         return "fails"
    #     except Exception as ex:
    #         response_object = {
    #             'status': 'fail',
    #             'message': 'Authorization: {}'.format(ex)
    #         }
    #         return response_object, 409

    def filter_date(self, req):
        data = json.loads(req.data)
        payload = jwt.decode(req.headers.get('Authorization'), key)
        if payload:
            data['user_id'] = payload['sub']
            all_currency = CurrencyModel.query.all()
            list_summary = []

            for currency in all_currency:
                balance = 0

                data['currency_id'] = currency.id
                # incomes =
                # print(incomes.income)
                latest_transaction = self.transaction_model.find_by_latest_transaction(data)
                income = self.transaction_model.filter_summary_income(data).income
                expenses = self.transaction_model.filter_summary_expenses(data).expenses
                if latest_transaction:
                    balance = latest_transaction.balance
                    print('latest_transaction: ', latest_transaction.id)
                data_summary = {
                    "currency_code": currency.code,
                    "balance": balance,
                    "income": income == "null" and income or 0,
                    "expenses": expenses == "null" and expenses or 0,
                }
                list_summary.append(data_summary)

            transactions = self.transaction_model.filter_created_at(payload['sub'], data)
            list_trans = []
            for transaction in transactions:
                trans = {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "content": transaction.content,
                    "user_id": transaction.user_id,
                    "created_at": transaction.created_at,
                    "updated_at": transaction.updated_at,
                    "currency_type": transaction.currency_id,
                    "action_type": transaction.action_type.value
                }
                list_trans.append(trans)
            return {
                "summary": list_summary,
                "result": list_trans
            }
        return "user not found"