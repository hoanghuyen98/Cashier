
from config import db, key


class CurrencyModel(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "currency"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    transactions = db.relationship('TransactionModel', backref='currency', lazy=True)

    @classmethod
    def find_all(self):
        return self.query.all()

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def add_currency(cls, data):
        currency = CurrencyModel(code=data['code'], description=data["description"])
        db.session.add(currency)
        db.session.commit()
        return "Add currency success", ""

    def update_currency(cls, currency, data):
        currency.code = data['code']
        currency.description = data['description']
        db.session.commit()
        return "Update currency success", ""

    def delete_currency(self, currency):
        try:
            db.session.delete(currency)
            db.session.commit()
            result = "Delete success", ""
        except Exception as ex:
            result = "", "update transaction Fail: {}".format(ex)
        return result

    def __repr__(self):
            return "<User '{}'>".format(self.currency_type)
