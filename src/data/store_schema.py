import mongoengine

TYPE = (
    ("C", "Children"),
    ("M", "Men"),
    ("W", "Women"),
)


class Product(mongoengine.Document):
    name = mongoengine.StringField(
        max_length=128, required=True, unique_with=["seller", "ptype"]
    )
    seller = mongoengine.StringField(max_length=128, required=True)
    ptype = mongoengine.StringField(max_length=1, choices=TYPE)
    price = mongoengine.FloatField(min_value=0.0)


SIZE = (
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
    ("XXL", "Extra Extra Large"),
)


class ProductItem(mongoengine.Document):
    #     https://stackoverflow.com/questions/10144852/how-can-i-create-unique-ids-for-embedded-documents-in-mongodb
    #     from bson.objectid import ObjectId
    #     _id = ObjectIdField( required=True, default=lambda: ObjectId() )
    product = mongoengine.ReferenceField(
        Product, reverse_delete_rule=mongoengine.CASCADE, unique_with=["size", "color"]
    )
    color = mongoengine.StringField(max_length=64, required=True)
    size = mongoengine.StringField(max_length=3, choices=SIZE, required=True)
    quantity = mongoengine.IntField(min_value=0, required=True)


class BasketItem(mongoengine.EmbeddedDocument):
    product_item = mongoengine.ReferenceField(ProductItem, unique=True)
    quantity = mongoengine.IntField(min_value=1, default=1, required=True)


class User(mongoengine.Document):
    email = mongoengine.EmailField(required=True, primary_key=True)
    first_name = mongoengine.StringField(max_length=64, required=True)
    last_name = mongoengine.StringField(max_length=64, required=True)
    city = mongoengine.StringField(max_length=64)
    address = mongoengine.StringField(max_length=256)
    telephone = mongoengine.StringField(max_length=32)
    password = mongoengine.StringField(max_length=256, required=True)
    basket_items = mongoengine.EmbeddedDocumentListField(document_type=BasketItem)


class Driver(mongoengine.Document):
    national_id = mongoengine.StringField(
        min_length=10, max_length=10, required=True, primary_key=True
    )
    first_name = mongoengine.StringField(max_length=64, required=True)
    last_name = mongoengine.StringField(max_length=64, required=True)
    telephone = mongoengine.StringField(max_length=32)
    plate_number = mongoengine.StringField(max_length=16)


DELIVERY_TYPES = (
    ("N", "Normal"),
    ("S", "Special"),
)
DELIVERY_STATUSES = (("P", "Pending"), ("R", "Registered"), ("C", "Completed"))


class Order(mongoengine.Document):
    user = mongoengine.ReferenceField(
        document_type=User, reverse_delete_rule=mongoengine.NULLIFY
    )
    date = mongoengine.DateField(required=True)
    items = mongoengine.EmbeddedDocumentListField(document_type=BasketItem)
    delivery_type = mongoengine.StringField(
        max_length=1, choices=DELIVERY_TYPES, default="N", required=True
    )
    delivery_status = mongoengine.StringField(
        max_length=1, choices=DELIVERY_STATUSES, default="P", required=True
    )


class Delivery(mongoengine.Document):
    date = mongoengine.DateField(required=True)
    capacity = mongoengine.IntField(required=True)
    driver = mongoengine.ReferenceField(Driver, reverse_delete_rule=mongoengine.NULLIFY)
    orders = mongoengine.ListField(mongoengine.ReferenceField(document_type=Order))


class Comment(mongoengine.Document):
    user = mongoengine.ReferenceField(
        document_type=User, reverse_delete_rule=mongoengine.NULLIFY
    )
    product = mongoengine.ReferenceField(
        Product, reverse_delete_rule=mongoengine.CASCADE
    )
    rating = mongoengine.IntField(min_value=0, max_value=5, required=True)
    text = mongoengine.StringField()
