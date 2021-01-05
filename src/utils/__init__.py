import datetime


def generate_national_id(fake, prev_national_ids):
    nat_id = fake.numerify(text="##########")
    while nat_id in prev_national_ids:
        nat_id = fake.numerify(text="##########")
    prev_national_ids.add(nat_id)
    return nat_id


def str_to_date(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d").date()


def drop_db(client, db_name):
    client.drop_database(db_name)
