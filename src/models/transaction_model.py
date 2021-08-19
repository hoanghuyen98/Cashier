from datetime import datetime, timedelta

from sqlalchemy import func

from config import db
import enum


class ACTION_TYPE(enum.Enum):
    deposits = 'deposits'
    withdrawals = 'withdrawals'

class TransactionModel(db.Model):
    """ User Model for storing user related details """
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float(precision=2), default=0.0)

    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    balance = db.Column(db.Float(precision=2), default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    updated_at = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))

    action_type = db.Column(db.Enum(ACTION_TYPE), default=ACTION_TYPE.deposits, nullable=False)


    @classmethod
    def find_by_id_and_name(self, id, user_id):
        return self.query.filter_by(id=id, user_id=user_id).first()
    @classmethod
    def find_by_latest_transaction(self, data):
        print("currency_id", data['currency_id'])
        return self.query.filter_by(user_id=data['user_id'], currency_id=data['currency_id']).order_by(TransactionModel.id.desc()).first()

    @classmethod
    def find_by_user_id(self, user_id):
        return self.query.filter_by(user_id=user_id).all()

    @classmethod
    def filter_summary_income(self, data):
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') + timedelta(days=1)
        return self.query.with_entities(func.sum(TransactionModel.amount).label('income')).filter_by(user_id=data['user_id'], currency_id=data['currency_id'], action_type="deposits").filter(self.created_at <= end_date,
                                                            self.created_at >= start_date).first()

    @classmethod
    def filter_summary_expenses(self, data):
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') + timedelta(days=1)
        return self.query.with_entities(func.sum(TransactionModel.amount).label('expenses')).filter_by(user_id=data['user_id'], currency_id=data['currency_id'], action_type="withdrawals").filter(self.created_at <= end_date,
                                                            self.created_at >= start_date).first()


    @classmethod
    def filter_created_at(self, user_id ,data):
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') + timedelta(days=1)
        return self.query.filter_by(user_id=user_id).filter(self.created_at <= end_date,
                                                            self.created_at >= start_date).all()

    @classmethod
    def add_transaction(self, data, user):
        try:
            transaction = TransactionModel(amount=data['amount'], content=data['content'], user_id=data['user_id'], currency_id=data['currency_id'], action_type=data['action_type'], balance=data['balance'])
            db.session.add(transaction)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Add transaction success.'
            }
            return response_object, 201
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Add transaction Fail: {}'.format(ex)
            }
            return response_object, 409

    @classmethod
    def update_transaction(self, transaction, data):
        try:
            transaction.content = data['content']
            transaction.updated_at = datetime.now()
            db.session.commit()
            result = "update transaction success", ""
        except Exception as ex:
            result = "", "update transaction Fail: {}".format(ex)
        return result

    @classmethod
    def delete_transaction(self, transaction):
        try:
            db.session.delete(transaction)
            db.session.commit()
            result = "Delete success", ""
        except Exception as ex:
            result = "", "update transaction Fail: {}".format(ex)
        return result

    def __repr__(self):
        return "<Transaction '{}'>".format(self.id)




