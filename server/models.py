from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    items = association_proxy('reviews', 'item')

    def to_dict(self, nested=False):
        print(f"Serializing Customer: {self.id}, {self.name}")
        if nested:
            return {
                'id': self.id,
                'name': self.name
            }
        return {
            'id': self.id,
            'name': self.name,
            'items': [review.item_id for review in self.reviews if review.item_id],
            'reviews': [review.id for review in self.reviews]
        }

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    def to_dict(self, nested=False):
        print(f"Serializing Item: {self.id}, {self.name}")
        if nested:
            return {
                'id': self.id,
                'name': self.name,
                'price': self.price
            }
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.id for review in self.reviews]
        }

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def to_dict(self, nested=False):
        print(f"Serializing Review: {self.id}, {self.comment}")
        if nested:
            return {
                'id': self.id,
                'comment': self.comment
            }
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'customer': self.customer.to_dict(nested=True) if self.customer else None,
            'item': self.item.to_dict(nested=True) if self.item else None
        }

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'
