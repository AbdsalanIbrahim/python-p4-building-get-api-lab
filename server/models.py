from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Define metadata with naming conventions
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize the database instance
db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    # serialize_rules ensures we don't serialize unwanted attributes
    serialize_rules = ('-baked_goods.bakery',)  # Exclude the nested baked goods when serializing

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    baked_goods = db.relationship('BakedGood', backref='bakery')

    def __repr__(self):
        return f'<Bakery {self.name}>'

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    # serialize_rules ensures we don't serialize unwanted attributes
    serialize_rules = ('-bakery.baked_goods',)  # Exclude the nested bakery when serializing

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    def __repr__(self):
        return f'<Baked Good {self.name}, ${self.price}>'
