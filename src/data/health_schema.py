import mongoengine


class Doctor(mongoengine.Document):
    national_id = mongoengine.StringField(
        min_length=10, max_length=10, required=True, unique=True
    )
    first_name = mongoengine.StringField(max_length=64, required=True)
    last_name = mongoengine.StringField(max_length=64, required=True)
    specialty = mongoengine.StringField(max_length=64, required=True)
    background = mongoengine.IntField(min_value=0, max_value=100, required=True)


class Patient(mongoengine.Document):
    national_id = mongoengine.StringField(
        min_length=10, max_length=10, required=True, unique=True
    )
    first_name = mongoengine.StringField(max_length=64, required=True)
    last_name = mongoengine.StringField(max_length=64, required=True)
    address = mongoengine.StringField(max_length=256)
    birthdate = mongoengine.DateField(required=True)
    password = mongoengine.StringField(max_length=256, required=True)
    doctor_id = mongoengine.ReferenceField(Doctor, required=True)


class Pharmacy(mongoengine.Document):
    name = mongoengine.StringField(max_length=256, required=True)
    address = mongoengine.StringField(max_length=256)
    telephone = mongoengine.StringField(max_length=32)


class Company(mongoengine.Document):
    name = mongoengine.StringField(max_length=64, required=True, unique=True)
    telephone = mongoengine.StringField(max_length=32)


class Contract(mongoengine.Document):
    text = mongoengine.StringField()
    start_date = mongoengine.DateField(required=True)
    end_date = mongoengine.DateField(required=True)
    pharmacy_id = mongoengine.ReferenceField(Pharmacy, required=True)
    company_id = mongoengine.ReferenceField(Company, required=True)


class Drug(mongoengine.Document):
    name = mongoengine.StringField(
        max_length=128,
        required=True,
        unique_with="company_id",
    )
    company_id = mongoengine.ReferenceField(Company, required=True)
    formula = mongoengine.StringField(max_length=128, required=True)


class Sale(mongoengine.Document):
    drug_id = mongoengine.ReferenceField(Drug, required=True, unique_with="pharmacy_id")
    pharmacy_id = mongoengine.ReferenceField(Pharmacy, required=True)
    price = mongoengine.FloatField(required=True)


class PrescriptionItem(mongoengine.EmbeddedDocument):
    drug_id = mongoengine.ReferenceField(Drug, required=True)
    quantity = mongoengine.IntField(min_value=0, required=True)


class Prescription(mongoengine.Document):
    date = mongoengine.DateField(required=True)
    items = mongoengine.EmbeddedDocumentListField(PrescriptionItem, required=True)
    doctor_id = mongoengine.ReferenceField(Doctor, required=True)
    patient_id = mongoengine.ReferenceField(Patient, required=True)
