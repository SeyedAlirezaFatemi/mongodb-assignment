import random

from faker import Faker

from src.utils import generate_national_id
from .data import drug_formulas, drug_names, specialties
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


def initialize_db():
    seed = 42
    Faker.seed(seed)
    random.seed(seed)
    fake = Faker()

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
