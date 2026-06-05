import time
import random
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error

# Database Connection Configuration
# Change 'your_password' to match your local MySQL root password!
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123', 
    'database': 'supply_chain_db'
}

CITIES = ["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"]
VEHICLES = ["Heavy Truck", "Box Truck", "Delivery Van"]
STATUSES = ["In-Transit", "Delayed", "Delivered", "Cancelled"]
DELAY_REASONS = ["Traffic congestion", "Adverse weather", "Mechanical issue", "Customs checkpoint", "Driver fatigue"]

def get_or_create_route(cursor, origin, destination):
    """Checks if route exists in Dim_Routes, inserts it if missing, and returns Route_ID."""
    cursor.execute("SELECT Route_ID FROM Dim_Routes WHERE Origin = %s AND Destination = %s", (origin, destination))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO Dim_Routes (Origin, Destination) VALUES (%s, %s)", (origin, destination))
        return cursor.lastrowid

def generate_and_insert_logistics(connection):
    cursor = connection.cursor()
    
    # Generate Data Points
    shipment_id = f"SHP-{random.randint(100000, 999999)}"
    origin = random.choice(CITIES)
    destination = random.choice([c for c in CITIES if c != origin])
    v_type = random.choice(VEHICLES)
    status = random.choices(STATUSES, weights=[0.60, 0.25, 0.12, 0.03], k=1)[0]
    
    if random.random() < 0.04: status = None # Data quality issue injection

    delay_minutes = 0
    delay_reason = "None"
    if status == "Delayed":
        delay_reason = random.choice(DELAY_REASONS)
        delay_minutes = random.choice([random.randint(30, 200), random.randint(600, 1200)])
    elif status == "Cancelled":
        delay_reason = "Route Blocked / Safety Incident"

    units_carried = random.randint(10, 800)
    base_holding_rate = round(random.uniform(1.20, 5.50), 2)
    penalty_multiplier = 1.5 if status == "Delayed" else 1.0
    total_holding_cost = round((units_carried * base_holding_rate) * penalty_multiplier, 2)
    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 1. Resolve Foreign Key relationship for Route
        route_id = get_or_create_route(cursor, origin, destination)
        
        # 2. Insert into Fact Table
        insert_query = """
            INSERT INTO Fact_Shipments 
            (Timestamp, Shipment_ID, Vehicle_Type, Route_ID, Status, Delay_Reason, Delay_Minutes, Units_Carried, Total_Holding_Cost_INR) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_tuple = (timestamp_now, shipment_id, v_type, route_id, status, delay_reason, delay_minutes, units_carried, total_holding_cost)
        
        cursor.execute(insert_query, data_tuple)
        connection.commit()
        print(f"✅ Successfully written to MySQL -> {shipment_id} | Status: {status} | Route ID: {route_id}")
        
    except Error as e:
        print(f"❌ Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()

if __name__ == "__main__":
    print("🔌 Establishing connection to local MySQL Warehouse...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("🚀 Connection Active. Live pipeline pouring data into MySQL tables. Press Ctrl+C to halt.\n")
            while True:
                generate_and_insert_logistics(conn)
                time.sleep(1) # Write one heavy logistics record per second
    except KeyboardInterrupt:
        print("\n🛑 Pipeline paused by user.")
    except Error as e:
        print(f"❌ Connection Failed: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("🔌 Connection safely terminated.")   