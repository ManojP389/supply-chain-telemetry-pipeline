-- =========================================================================
-- 1. DATABASE & ARCHITECTURE SETUP (DDL)
-- =========================================================================
CREATE DATABASE IF NOT EXISTS supply_chain_db;
USE supply_chain_db;

-- Drop tables if they exist to allow clean, repeatable deployments
DROP TABLE IF EXISTS fact_shipments;
DROP TABLE IF EXISTS dim_vehicles;
DROP TABLE IF EXISTS dim_routes;

-- Create Fleet Dimension Table
CREATE TABLE dim_vehicles (
    Vehicle_ID INT AUTO_INCREMENT PRIMARY KEY,
    Vehicle_Type VARCHAR(50) NOT NULL,
    Max_Capacity INT NOT NULL,
    Speed_MPH INT NOT NULL
);

-- Create Route/Geography Dimension Table
CREATE TABLE dim_routes (
    Route_ID INT AUTO_INCREMENT PRIMARY KEY,
    Origin VARCHAR(50) NOT NULL,
    Destination VARCHAR(50) NOT NULL
);

-- Create Central Transactional Fact Table
CREATE TABLE fact_shipments (
    Shipment_ID VARCHAR(50) PRIMARY KEY,
    Vehicle_ID INT,
    Route_ID INT,
    Timestamp DATETIME NOT NULL,
    Raw_Status VARCHAR(50),
    Delay_Reason VARCHAR(100),
    Adjusted_Delay_Minutes INT DEFAULT 0,
    Total_Cost_INR DECIMAL(12,2) DEFAULT 0.00,
    FOREIGN KEY (Vehicle_ID) REFERENCES dim_vehicles(Vehicle_ID),
    FOREIGN KEY (Route_ID) REFERENCES dim_routes(Route_ID)
);

-- =========================================================================
-- 2. SEED SELECTION DATA (Dimension Population)
-- =========================================================================
INSERT INTO dim_vehicles (Vehicle_Type, Max_Capacity, Speed_MPH) VALUES 
('Box Truck', 500, 55),
('Delivery Van', 150, 65),
('Heavy Truck', 1200, 45);

INSERT INTO dim_routes (Origin, Destination) VALUES 
('Kolkata', 'Delhi'),
('Kolkata', 'Hyderabad'),
('Kolkata', 'Mumbai'),
('Kolkata', 'Pune'),
('Mumbai', 'Ahmedabad'),
('Mumbai', 'Bengaluru'),
('Mumbai', 'Chennai'),
('Mumbai', 'Delhi'),
('Mumbai', 'Hyderabad'),
('Mumbai', 'Kolkata'),
('Mumbai', 'Pune'),
('Pune', 'Ahmedabad'),
('Pune', 'Bengaluru');

-- =========================================================================
-- 3. ANALYTICAL DATA-CLEANSING & ANOMALY LOGIC VIEW
-- =========================================================================
CREATE OR REPLACE VIEW v_clean_shipments AS
SELECT 
    f.Shipment_ID,
    v.Vehicle_Type,
    r.Origin,
    r.Destination,
    f.Timestamp,
    
    -- Impute missing or corrupted string statuses
    CASE 
        WHEN f.Raw_Status IS NULL OR f.Raw_Status = '' THEN 'Unknown/Missing'
        ELSE f.Raw_Status 
    END AS Cleaned_Status,
    
    f.Delay_Reason,
    f.Adjusted_Delay_Minutes,
    f.Total_Cost_INR,
    
    -- Dynamic Pipeline Anomaly Classification Flags
    CASE 
        WHEN f.Raw_Status = 'Cancelled' AND f.Adjusted_Delay_Minutes > 0 THEN 'Data Entry Error'
        WHEN f.Adjusted_Delay_Minutes > 180 THEN 'Critical Operational Outlier'
        ELSE 'Normal Operational Variance'
    END AS Operational_Anomalies
FROM fact_shipments f
LEFT JOIN dim_vehicles v ON f.Vehicle_ID = v.Vehicle_ID
LEFT JOIN dim_routes r ON f.Route_ID = r.Route_ID;