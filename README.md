#  Supply Chain Logistics & Bottleneck Optimization Console

An end-to-end, enterprise-grade **Data Engineering & Business Intelligence** project that simulates real-world logistics operations and transforms raw telemetry data into actionable business insights.

This project demonstrates a complete scalable data pipeline—from Python-based shipment telemetry generation, relational data warehousing in MySQL, automated data cleansing through SQL views, and real-time visualization using Power BI.

---
<img width="1312" height="737" alt="image" src="https://github.com/user-attachments/assets/097ef525-676c-4fe0-bee3-de08a53b35a5" />


## Project Overview

Modern logistics operations generate massive amounts of data from vehicles, routes, and shipment events. This project builds a complete analytics ecosystem capable of:

* Simulating live fleet telemetry streams
* Storing operational data in a structured warehouse
* Cleaning and transforming raw records automatically
* Detecting bottlenecks and operational risks
* Monitoring logistics KPIs in real time
* Providing executive-level decision support dashboards

---

##  Dashboard Features

### Executive KPI Scorecards

Track critical logistics metrics including:

* Total Shipments Processed
* Total Financial Loss (INR)
* Average Delivery Duration
* Maximum Delay Minutes
* Delay Incident Percentage

### Root Cause Analysis

Identify major disruption categories:

* Traffic Congestion
* Weather Conditions
* Mechanical Failures
* Customs Delays

### Financial Leakage Tracking

Analyze cumulative penalties and losses across:

* Origin Locations
* Destination Routes
* Shipping Corridors

### Shipment Velocity Funnel

Visualize shipment movement through operational stages:

```text
In Transit
    ↓
Delayed
    ↓
Delivered
    ↓
Cancelled
```

### Compliance Monitoring

Gauge visualization tracks:

* Delay Incident Rate
* Corporate Threshold Compliance
* Operational Risk Levels

### Operational Ledger

Detailed transactional records including:

* Shipment IDs
* Vehicle Information
* Route Data
* Delay Metrics
* Cost Impact
* Data Quality Flags

---

##  System Architecture

```text
┌──────────────────────┐
│ 1. INGESTION LAYER   │
│ Python Telemetry Sim │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 2. STORAGE LAYER     │
│ MySQL Data Warehouse │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 3. ANALYTICS LAYER   │
│ SQL Views & Cleansing│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ 4. VISUALIZATION     │
│ Power BI Dashboard   │
└──────────────────────┘
```

---

##  Pipeline Layers

### 1️ Ingestion Layer (Python)

A Python-based telemetry simulator generates realistic logistics data from multiple vehicle categories:

* Box Trucks
* Heavy Trucks
* Delivery Vans

The simulator intentionally introduces real-world data issues:

* Missing locations
* Inconsistent statuses
* Variable reporting intervals
* Delayed updates

This ensures downstream systems are tested against realistic operational challenges.

---

### 2️ Storage Layer (MySQL Warehouse)

Raw telemetry is transformed into a structured **Star Schema** for analytical efficiency.

#### Fact Table

**fact_shipments**

Stores:

* Shipment Events
* Delay Minutes
* Cost Impact
* Delivery Status
* Timestamps

#### Dimension Tables

**dim_vehicles**

Stores:

* Vehicle Type
* Speed Limits
* Capacity Constraints

**dim_routes**

Stores:

* Origin Locations
* Destination Locations
* Route Metadata

---

### 3️ Analytics Layer (SQL Views)

Instead of exposing raw production tables directly, analytical views provide a secure transformation layer.

#### View: `v_clean_shipments`

Responsibilities:

* Missing value handling
* Status normalization
* Data quality improvements
* Outlier classification
* Cost calculations

Generated fields include:

* Total Cost INR
* Delay Categories
* Operational Risk Flags
* Data Cleansing Indicators

---

### 4️ Visualization Layer (Power BI)

The cleaned warehouse views are connected to Power BI through an ODBC connector.

Benefits:

* Fast dashboard performance
* Backend query optimization
* Instant slicer interactions
* Real-time KPI refreshes
* Executive-level reporting

---

##  Repository Structure

```text
Supply-Chain-Optimization/
│
├── database/
│   └── star_schema_setup.sql
│
├── ingestion/
│   └── telemetry_generator.py
│
├── dashboard/
│   └── bottleneck_console.pbit
│
|
│
└── README.md
```

---

## 🛠️ Technology Stack

| Layer           | Technology   |
| --------------- | ------------ |
| Data Generation | Python       |
| Database        | MySQL        |
| Data Modeling   | Star Schema  |
| Data Cleaning   | SQL Views    |
| Connectivity    | ODBC         |
| Visualization   | Power BI     |
| Version Control | Git & GitHub |

---

## 🚀Local Setup

### Prerequisites

Install:

* Python 3.x
* MySQL Server
* mysql-connector-python or SQLAlchemy
* Power BI Desktop

---

### Step 1: Initialize Database

```bash
mysql -u your_username -p < database/star_schema_setup.sql
```

This creates:

* Fact Tables
* Dimension Tables
* Views
* Relationships
* Indexes

---

### Step 2: Run Data Ingestion

Update database credentials inside:

```python
telemetry_generator.py
```

Execute:

```bash
python ingestion/telemetry_generator.py
```

The simulator will begin generating logistics telemetry records.

---

### Step 3: Launch Power BI

Open:

```text
dashboard/bottleneck_console.pbit
```

Provide:

* MySQL Server Credentials
* ODBC Connection Details

Click:

```text
Home → Refresh
```

The dashboard will automatically populate with warehouse data.

---

##  Business Value

This project demonstrates practical skills in:

* Data Engineering
* Data Warehousing
* ETL Pipeline Design
* SQL Optimization
* Business Intelligence
* Power BI Dashboard Development
* Supply Chain Analytics
* Root Cause Analysis
* KPI Monitoring

---

##  Future Enhancements

Potential improvements:

* Real-time Kafka Streaming
* Dockerized Deployment
* Cloud Warehouse Integration
* Predictive Delay Forecasting
* Machine Learning Risk Models
* Fleet Route Optimization
* Live GPS Integration
* Automated Alerting System

---
## 🚀 Deployment & Local Setup Instructions

### Prerequisites
* **Python 3.x** (with `mysql-connector-python` or `SQLAlchemy` installed)
* **MySQL Server** instance initialized locally
* **Power BI Desktop** (Windows environment)


## License

This project is intended for educational, portfolio, and demonstration purposes.

---

### ⭐ If you found this project useful, consider giving the repository a star.
