"""Generate simulated SAP master data (MARA, LFA1) into the sap_sim Postgres DB."""
import os
import random
from datetime import date, timedelta
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from faker import Faker

load_dotenv(Path(__file__).resolve().parents[2] / "infra" / ".env")

SEED = 42
N_MATERIALS = 300
N_VENDORS = 60

random.seed(SEED)
Faker.seed(SEED)
fake = Faker("es_AR")


def random_date(start_year=2018, end_year=2025):
    start = date(start_year, 1, 1)
    return start + timedelta(days=random.randint(0, (date(end_year, 12, 31) - start).days))


def make_materials():
    words = ["Valvula", "Rodamiento", "Bomba", "Sensor", "Cable", "Brida",
             "Filtro", "Motor", "Junta", "Tuberia", "Tornillo", "Transmisor"]
    specs = ["DN50", "DN100", "1/2in", "3/4in", "24V", "220V", "AISI304", "PN16"]
    groups = ["MECANICA", "ELECTRICA", "INSTRUM", "TUBERIAS", "LUBRIC"]
    rows = []
    for i in range(N_MATERIALS):
        matnr = f"{100000 + i:018d}"
        maktx = f"{random.choice(words)} {random.choice(specs)}"
        mtart = random.choices(["ROH", "HALB", "FERT"], weights=[60, 25, 15])[0]
        matkl = random.choice(groups)
        meins = random.choice(["EA", "KG", "M", "L"])
        brgew = round(random.uniform(0.05, 250), 3)
        # intentional dirt
        r = random.random()
        if r < 0.05:
            maktx = f"  {maktx}  "
        elif r < 0.09:
            maktx = maktx.upper()
        if random.random() < 0.03:
            matkl = None
        rows.append((matnr, maktx[:40], mtart, matkl, meins, brgew, random_date()))
    return rows


def make_vendors():
    rows = []
    for i in range(N_VENDORS):
        lifnr = f"{200000 + i:010d}"
        name1 = fake.company()[:35]
        land1 = random.choice(["AR", "CL", "BR", "UY", "PY", "US", "DE", "CN"])
        ort01 = fake.city()[:35]
        ktokk = random.choice(["KRED", "LIEF"])
        # intentional dirt
        r = random.random()
        if r < 0.05:
            name1 = f"  {name1.lower()}  "
        if random.random() < 0.05:
            ort01 = None
        rows.append((lifnr, name1[:35], land1, ort01, ktokk, random_date()))
    return rows


def main():
    conn = psycopg.connect(
        host="localhost",
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    with conn, conn.cursor() as cur:
        cur.execute("TRUNCATE mara, lfa1 CASCADE")
        cur.executemany(
            "INSERT INTO mara (matnr, maktx, mtart, matkl, meins, brgew, ersda) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)", make_materials())
        cur.executemany(
            "INSERT INTO lfa1 (lifnr, name1, land1, ort01, ktokk, erdat) "
            "VALUES (%s, %s, %s, %s, %s, %s)", make_vendors())
    print(f"Loaded {N_MATERIALS} materials and {N_VENDORS} vendors.")


if __name__ == "__main__":
    main()
