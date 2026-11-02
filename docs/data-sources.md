# Data sources

Both sources are simulated and fully reproducible (fixed random seeds).

## SAP-like source (PostgreSQL, database `sap_sim`)

| Table | Description | Rows |
|---|---|---|
| `mara` | Material master | 300 |
| `lfa1` | Vendor master | 60 |
| `ekko` / `ekpo` | Purchase orders (header / items) | 800 / ~2,400 |
| `vbak` / `vbap` | Sales orders (header / items) | 1,500 / ~3,700 |

Generators: `sources/sap/generate_sap_data.py` (seed 42) and
`sources/sap/generate_sap_transactions.py` (seed 43). Run them in that order.

## SCADA-like source (JSON Lines)

18 sensors (2 plants x 3 equipment x 3 metrics: temperature, pressure, flow),
one reading every 10 seconds. Generator: `sources/scada/generate_scada_data.py` (seed 44).

Event shape: `sensor_id`, `plant`, `equipment`, `metric`, `unit`, `value`, `quality`, `ts`.

## Intentional data defects

These are injected on purpose, to be detected and handled in later phases.

| Source | Defect | Approx. rate |
|---|---|---|
| `mara.maktx` | Leading/trailing spaces | 5% |
| `mara.maktx` | All uppercase | 4% |
| `mara.matkl` | NULL material group | 3% |
| `lfa1.name1` | Lowercase with extra spaces | 5% |
| `lfa1.ort01` | NULL city | 5% |
| `ekko.waers` | Lowercase currency code | 3% |
| `ekko.ernam` | NULL created-by user | 2% |
| `ekpo.netpr` | Zero net price | 1% |
| SCADA | `BAD` quality with NULL value | 1% |
| SCADA | `UNCERTAIN` quality | 1% |
| SCADA | Duplicate events | 0.5% |
| SCADA | Spikes (value x0.4 or x1.8) | 0.3% |
| SCADA | Drift on `PLANT_N.PUMP_02.PRESSURE` (up to +15%) | last third of the series |

Note: `vbak.kunnr` has no foreign key yet (no customer master table).
