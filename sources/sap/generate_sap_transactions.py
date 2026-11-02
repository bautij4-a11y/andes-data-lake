"""Generate simulated SAP transactional data (EKKO, EKPO, VBAK, VBAP).

Run AFTER generate_sap_data.py: it reads the existing MARA and LFA1 keys.
"""
import os
import random
from datetime import date, timedelta
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / "infra" / ".env")

SEED = 43
N_PURCHASE_ORDERS = 800
N_SALES_ORDERS = 1500
N_CUSTOMERS = 50

random.seed(SEED)

USERS = ["JPEREZ", "MGOMEZ", "LRUIZ", "AFERNANDEZ", "SLOPEZ"]


def random_date(start=date(2024, 1, 1), end=date(2025, 12, 31)):
    return start + timedelta(days=random.randint(0, (end - start).days))


def make_purchases(materials, vendors, base_price):
    headers, items = [], []
    for i in range(N_PURCHASE_ORDERS):
        ebeln = f"{4500000000 + i}"
        waers = random.choice(["USD", "ARS", "EUR"])
        ernam = random.choice(USERS)
        # intentional dirt
        if random.random() < 0.03:
            waers = waers.lower()
        if random.random() < 0.02:
            ernam = None
        headers.append((ebeln, random.choice(vendors), random.choice(["NB", "FO"]),
                        random_date(), waers, ernam))
        for j, (matnr, meins) in enumerate(random.sample(materials, random.randint(1, 5))):
            netpr = round(base_price[matnr] * random.uniform(0.9, 1.1), 2)
            if random.random() < 0.01:
                netpr = 0  # intentional dirt: zero price
            items.append((ebeln, f"{(j + 1) * 10:05d}", matnr,
                          round(random.uniform(1, 500), 3), meins, netpr))
    return headers, items


def make_sales(materials, base_price):
    headers, items = [], []
    for i in range(N_SALES_ORDERS):
        vbeln = f"{5000000000 + i}"
        kunnr = f"{300000 + random.randint(0, N_CUSTOMERS - 1):010d}"
        headers.append((vbeln, random.choice(["OR", "ZOR"]), random_date(),
                        kunnr, random.choice(["USD", "ARS"])))
        for j, (matnr, meins) in enumerate(random.sample(materials, random.randint(1, 4))):
            qty = round(random.uniform(1, 200), 3)
            netwr = round(qty * base_price[matnr] * 1.3, 2)
            items.append((vbeln, f"{(j + 1) * 10:06d}", matnr, qty, meins, netwr))
    return headers, items


def main():
    conn = psycopg.connect(
        host="localhost",
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    with conn, conn.cursor() as cur:
        cur.execute("SELECT matnr, meins FROM mara ORDER BY matnr")
        materials = cur.fetchall()
        cur.execute("SELECT lifnr FROM lfa1 ORDER BY lifnr")
        vendors = [r[0] for r in cur.fetchall()]
        base_price = {m: round(random.uniform(5, 2000), 2) for m, _ in materials}

        ekko, ekpo = make_purchases(materials, vendors, base_price)
        vbak, vbap = make_sales(materials, base_price)

        cur.execute("TRUNCATE ekpo, ekko, vbap, vbak")
        cur.executemany("INSERT INTO ekko VALUES (%s, %s, %s, %s, %s, %s)", ekko)
        cur.executemany("INSERT INTO ekpo VALUES (%s, %s, %s, %s, %s, %s)", ekpo)
        cur.executemany("INSERT INTO vbak VALUES (%s, %s, %s, %s, %s)", vbak)
        cur.executemany("INSERT INTO vbap VALUES (%s, %s, %s, %s, %s, %s)", vbap)
    print(f"Loaded {len(ekko)} PO headers, {len(ekpo)} PO items, "
          f"{len(vbak)} sales headers, {len(vbap)} sales items.")


if __name__ == "__main__":
    main()
