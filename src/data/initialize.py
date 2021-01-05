import random

from faker import Faker

from src.utils import generate_national_id
from .data import drug_formulas, drug_names, product_names, specialties
from .health_schema import (
    Company,
    Contract,
    Doctor,
    Drug,
    Patient,
    Pharmacy,
    Prescription,
    PrescriptionItem,
    Sale,
)
from .store_schema import (
    BasketItem,
    Comment,
    Driver,
    Product,
    ProductItem,
    SIZE,
    TYPE,
    User,
)


def initialize_db():
    seed = 42
    Faker.seed(seed)
    random.seed(seed)
    fake = Faker()
    #################
    # Health System #
    #################
    docs_national_ids = set()
    patients_national_ids = set()
    doctors = []
    patients = []
    pharmacies = []
    companies = []
    drugs = []
    for _ in range(100):
        doctor = Doctor(
            **{
                "national_id": generate_national_id(fake, docs_national_ids),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "specialty": random.choice(specialties),
                "background": random.randint(0, 80),
            }
        )
        doctor.save()
        doctors.append(doctor)

        patient = Patient(
            **{
                "national_id": generate_national_id(fake, patients_national_ids),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "address": fake.address(),
                "birthdate": fake.profile(fields=["birthdate"])["birthdate"],
                "password": fake.profile(fields=["username"])["username"],
                "doctor_id": random.choice(doctors),
            }
        )
        patient.save()
        patients.append(patient)

        pharmacy = Pharmacy(
            **{
                "name": fake.company(),
                "address": fake.address(),
                "telephone": fake.phone_number(),
            }
        )
        pharmacy.save()
        pharmacies.append(pharmacy)

        company = Company(
            **{
                "name": fake.company(),
                "telephone": fake.phone_number(),
            }
        )
        company.save()
        companies.append(company)

        contract = Contract(
            **{
                "text": fake.paragraph(nb_sentences=5),
                "start_date": fake.date_this_decade(
                    before_today=True, after_today=False
                ),
                "end_date": fake.future_date(),
                "pharmacy_id": random.choice(pharmacies),
                "company_id": random.choice(companies),
            }
        )
        contract.save()

    for company in companies:
        for drug_name in random.sample(drug_names, random.randint(1, 20)):
            drug = Drug(
                **{
                    "name": drug_name,
                    "formula": random.choice(drug_formulas),
                    "company_id": company,
                }
            )
            drug.save()
            drugs.append(drug)

    for pharmacy in pharmacies:
        for drug in random.sample(drugs, random.randint(1, 20)):
            sale = Sale(
                **{
                    "drug_id": drug,
                    "pharmacy_id": pharmacy,
                    "price": random.uniform(20, 1000),
                }
            )
            sale.save()

    for _ in range(100):
        items = []
        for _ in range(random.randint(1, 20)):
            item = PrescriptionItem(
                **{
                    "drug_id": random.choice(drugs),
                    "quantity": random.randint(1, 10),
                }
            )
            items.append(item)
        prescription = Prescription(
            **{
                "date": fake.date_this_decade(before_today=True, after_today=False),
                "items": items,
                "doctor_id": random.choice(doctors),
                "patient_id": random.choice(patients),
            }
        )
        prescription.save()
    ################
    # Store System #
    ################
    products = []
    product_items = []
    users = []
    for _ in range(100):
        seller = fake.company()
        for i in range(random.randint(1, 3)):
            product = Product(
                **{
                    "name": random.choice(product_names),
                    "seller": seller,
                    "ptype": TYPE[i][0],
                    "price": random.uniform(20, 1000),
                }
            )
            product.save()
            products.append(product)

    for product in products:
        for i in range(random.randint(1, 4)):
            product_item = ProductItem(
                **{
                    "product_id": product,
                    "color": fake.color_name(),
                    "size": SIZE[i][0],
                    "quantity": random.randint(0, 500),
                }
            )
            product_item.save()
            product_items.append(product_item)

    for _ in range(100):
        basket = []
        for product_item in random.sample(product_items, random.randint(1, 10)):
            basket.append(
                BasketItem(
                    **{
                        "product_item_id": product_item,
                        "quantity": random.randint(1, 5),
                    }
                )
            )
        profile = fake.profile(["mail", "username", "address"])
        user = User(
            **{
                "email": profile["mail"],
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "address": profile["address"],
                "password": profile["username"],
                "city": fake.city(),
                "telephone": fake.phone_number(),
                "basket": basket,
            }
        )
        user.save()
        users.append(user)

        driver = Driver(
            **{
                "national_id": generate_national_id(fake, patients_national_ids),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "telephone": fake.phone_number(),
                "license_plate": fake.license_plate(),
            }
        )
        driver.save()
        comment = Comment(
            **{
                "user_id": random.choice(users),
                "product_id": random.choice(products),
                "text": fake.sentence(nb_words=10),
                "rating": random.randint(0, 5),
            }
        )
        comment.save()
