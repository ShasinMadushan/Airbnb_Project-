# Airbnb London Market Analysis: End-to-End Data Pipeline

## 📌 Project Overview
This project is a complete end-to-end data engineering and analytics pipeline designed to analyze Airbnb listings in the London market. The goal is to uncover actionable business insights regarding geographic pricing gradients, host behavior (Superhost status), and market distribution.

## 🏗️ Architecture & Tech Stack
This project implements a decoupled data architecture, separating the heavy data transformations from the final visualization layer to ensure high performance and scalability.

* **Data Processing:** Python (`pandas`)
* **Local Data Warehouse:** DuckDB (In-process analytical database)
* **Optimized Storage:** Parquet (Columnar storage for BI performance)
* **Visualization Layer:** Microsoft Power BI

## 📂 Project Structure
```text
Airbnb_Project/
├── data/
│   ├── raw/                  # Compressed raw CSV files (e.g., london_listings.csv.gz)
│   └── processed/            # Cleaned database (airbnb.duckdb) and exports (.parquet)
├── src/
│   └── transformation/
│       ├── clean_listings.py     # Core ELT script (handles nulls, types, standardization)
│       └── export_to_parquet.py  # Pipeline stage to generate BI-ready Parquet files
├── dashboard/                # Power BI (.pbix) and PDF exports
└── README.md
🛠️ Engineering Decision Log
During the development of this pipeline, several architectural decisions were made to prioritize data quality and system stability:

DuckDB for Local Analytics: Selected DuckDB over traditional RDBMS systems to leverage its vectorized query execution on local hardware without the overhead of server management.

Strict Data Quality Gates: Implemented hard validation in clean_listings.py. Rows with critical missing values (e.g., price) are explicitly dropped during the Python transformation phase, ensuring 100% data integrity before it reaches the Gold/Presentation layer.

Parquet Integration over ODBC: Initially evaluated connecting Power BI directly to DuckDB via ODBC. Pivoted to a decoupled Parquet export strategy to bypass local environment dependencies, eliminate authentication bottlenecks, and natively preserve schema data types for Power BI.

📊 Key Business Insights
(Note: See the exported PDF dashboard for visual context)

Geographic Pricing Gradients: Mapped the concentration of high-value listings, highlighting premium pricing zones in central London compared to outer boroughs.

Superhost Market Share: Analyzed the distinct count of properties managed by Superhosts vs. standard hosts to determine market concentration.

Room Type Revenue Drivers: Segmented inventory by room type to identify the most frequent listing configurations (e.g., Entire Home vs. Private Room).

🚀 How to Run the Pipeline
Clone the repository and activate your virtual environment.

Execute the data cleaning and loading script:

         python src/transformation/clean_listings.py
         
Generate the BI-ready Parquet file:

        python src/transformation/export_to_parquet.py