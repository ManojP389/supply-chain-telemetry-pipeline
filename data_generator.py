import time
import random
from datetime import datetime, timedelta
import json

# Operational Configurations
CITIES = ["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"]
VEHICLES = {
    "Heavy Truck": {"speed_mph": 45, "capacity": 1000},
    "Box Truck": {"speed_mph": 55, "capacity": 500},
    "Delivery Van": {"speed_mph": 65, "capacity": 150}
}
STATUSES = ["In-Transit", "Delayed", "Delivered", "Cancelled"]
DELAY_REASONS = ["Traffic congestion", "Adverse weather", "Mechanical issue", "Customs checkpoint", "Driver fatigue"]

def generate_advanced_logistics_record():
    shipment_id = f"SHP-{random.randint(100000, 999999)}"
    origin = random.choice(CITIES)
    destination = random.choice([c for c in CITIES if c != origin])
    
    v_type = random.choice(list(VEHICLES.keys()))
    status = random.choices(STATUSES, weights=[0.60, 0.25, 0.12, 0.03], k=1)[0]
    
    # 1. Injecting Real-World Data Anomaly (Data Cleaning Practice)
    # 4% of the time, the status might be missing or corrupted (None)
    if random.random() < 0.04:
        status = None

    # 2. Advanced Delay & Operational Logic
    delay_minutes = 0
    delay_reason = "None"
    if status == "Delayed":
        delay_reason = random.choice(DELAY_REASONS)
        # Injecting an outlier: standard delay is 30-200 mins, occasionally an extreme 1200 mins breakdown
        delay_minutes = random.choice([random.randint(30, 200), random.randint(600, 1200)])
    elif status == "Cancelled":
        delay_reason = "Route Blocked / Safety Incident"

    # 3. Financial Cost Modeling
    units_carried = random.randint(10, VEHICLES[v_type]["capacity"])
    # Base holding cost per unit per hour in INR
    base_holding_rate = round(random.uniform(1.20, 5.50), 2)
    
    # Critical Business Metric: Penalize delays financially
    penalty_multiplier = 1.5 if status == "Delayed" else 1.0
    total_holding_cost = round((units_carried * base_holding_rate) * penalty_multiplier, 2)
    
    # 4. Temporal Data Processing
    timestamp_now = datetime.now()
    base_travel_time = random.randint(4, 24)
    estimated_delivery = timestamp_now + timedelta(hours=base_travel_time) + timedelta(minutes=delay_minutes)

    return {
        "timestamp": timestamp_now.strftime("%Y-%m-%d %H:%M:%S"),
        "shipment_id": shipment_id,
        "vehicle_type": v_type,
        "origin": origin,
        "destination": destination,
        "status": status,
        "delay_reason": delay_reason,
        "delay_minutes": delay_minutes,
        "units_carried": units_carried,
        "total_holding_cost_inr": total_holding_cost
    }

if __name__ == "__main__":
    print("💎 Production-Grade Supply Chain Stream Initialized...")
    print("📦 Generating dirty, live business events. Press Ctrl+C to stop.\n")
    try:
        while True:
            record = generate_advanced_logistics_record()
            print(json.dumps(record, indent=2))
            print("="*50)
            time.sleep(1.5) # Simulating rapid stream events
    except KeyboardInterrupt:
        print("\nPipeline execution paused.")