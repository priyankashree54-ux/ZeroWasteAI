"""I could not find a real dataset of leftover food, so this file makes a practice one.
The numbers follow simple logic (more food cooked = more leftover, more customers = less leftover)."""
import numpy as np, pandas as pd

VENDOR_TYPES = ["Restaurant", "Bakery", "Caterer", "Hostel Mess", "Supermarket"]
BASE = {"Restaurant": 12, "Bakery": 9, "Caterer": 30, "Hostel Mess": 22, "Supermarket": 18}

def generate(n=4000, seed=42):
    rng = np.random.default_rng(seed)
    vt = rng.choice(VENDOR_TYPES, n)
    day = rng.integers(0, 7, n)                  # 0=Mon .. 6=Sun
    prepared = rng.integers(40, 400, n)          # how much food was cooked
    footfall = rng.integers(20, 500, n)          # how many people were expected
    festival = rng.choice([0, 1], n, p=[0.88, 0.12])
    rain = rng.choice([0, 1], n, p=[0.8, 0.2])
    base = np.array([BASE[v] for v in vt])
    surplus = (base + 0.18 * prepared - 0.10 * footfall
               + 6 * (day >= 5) + 9 * festival + 7 * rain
               + rng.normal(0, 4, n))
    surplus = np.clip(surplus, 0, None).round(1)
    return pd.DataFrame(dict(vendor_type=vt, day_of_week=day, meals_prepared=prepared,
                             expected_footfall=footfall, festival=festival, rain=rain,
                             surplus_kg=surplus))

if __name__ == "__main__":
    generate().to_csv("surplus_data.csv", index=False)
    print("saved surplus_data.csv")
