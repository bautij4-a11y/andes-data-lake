"""Generate simulated SCADA sensor readings as JSON Lines (one reading per line).

In Phase 2 the same events will be published to Kafka instead of a file.
"""
import argparse
import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

SEED = 44

# (metric, unit, base value, daily-cycle amplitude, noise std)
METRICS = [
    ("temperature", "C", 60.0, 5.0, 0.5),
    ("pressure", "bar", 6.0, 0.5, 0.08),
    ("flow", "m3_h", 120.0, 15.0, 2.0),
]
PLANTS = ["PLANT_N", "PLANT_S"]
EQUIPMENT = ["PUMP_01", "PUMP_02", "COMPRESSOR_01"]


def build_sensors(rng):
    sensors = []
    for plant in PLANTS:
        for eq in EQUIPMENT:
            for metric, unit, base, amp, noise in METRICS:
                sensors.append({
                    "sensor_id": f"{plant}.{eq}.{metric}".upper(),
                    "plant": plant,
                    "equipment": eq,
                    "metric": metric,
                    "unit": unit,
                    "base": base * rng.uniform(0.95, 1.05),
                    "amp": amp,
                    "noise": noise,
                    "phase": rng.uniform(0, 2 * math.pi),
                })
    return sensors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", type=int, default=60)
    parser.add_argument("--interval", type=int, default=10, help="seconds between readings")
    parser.add_argument("--start", default="2025-12-01T00:00:00")
    parser.add_argument("--output", default=str(Path(__file__).parent / "data" / "readings.jsonl"))
    args = parser.parse_args()

    rng = random.Random(SEED)
    sensors = build_sensors(rng)
    start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc)
    n_steps = args.minutes * 60 // args.interval
    drift_sensor = sensors[4]["sensor_id"]
    drift_start = int(n_steps * 2 / 3)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    n_events = 0
    with out.open("w") as f:
        for step in range(n_steps):
            ts = start + timedelta(seconds=step * args.interval)
            for s in sensors:
                cycle = math.sin(2 * math.pi * step / max(n_steps, 1) + s["phase"])
                value = s["base"] + s["amp"] * cycle + rng.gauss(0, s["noise"])
                if rng.random() < 0.003:                      # anomalous spike
                    value *= rng.choice([0.4, 1.8])
                if s["sensor_id"] == drift_sensor and step > drift_start:  # slow drift
                    value += s["base"] * 0.15 * (step - drift_start) / (n_steps - drift_start)
                quality = "GOOD"
                r = rng.random()
                if r < 0.01:                                  # missing value
                    quality, value = "BAD", None
                elif r < 0.02:
                    quality = "UNCERTAIN"
                event = {
                    "sensor_id": s["sensor_id"],
                    "plant": s["plant"],
                    "equipment": s["equipment"],
                    "metric": s["metric"],
                    "unit": s["unit"],
                    "value": None if value is None else round(value, 3),
                    "quality": quality,
                    "ts": ts.isoformat().replace("+00:00", "Z"),
                }
                line = json.dumps(event)
                f.write(line + "\n")
                n_events += 1
                if rng.random() < 0.005:                      # duplicate event
                    f.write(line + "\n")
                    n_events += 1
    print(f"Wrote {n_events} readings from {len(sensors)} sensors to {out}")


if __name__ == "__main__":
    main()
