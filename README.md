# Global Airbnb Market Analysis & Predictive Modeling

## Project Overview
This project is an end-to-end Data Engineering and Machine Learning pipeline analyzing the global Airbnb market across three major cities (London, Tokyo, NYC). It features an automated ELT architecture, multi-currency financial harmonization, predictive pricing models, and a custom Natural Language Processing (NLP) engine to analyze over 2 million guest reviews.

## Core Architecture & Tech Stack
* **Data Warehouse:** DuckDB (Local, columnar analytics)
* **Data Engineering (ELT):** Python (Pandas)
* **Machine Learning & Stats:** R (RandomForest, DBI, effsize)
* **Artificial Intelligence (NLP):** Python (VADER SentimentIntensityAnalyzer)
* **Infrastructure:** Docker & Docker Compose

## Key Features & Pipeline Steps
1. **Global Data Ingestion & Transformation:** Extracted >100,000 raw listings across three continents. Engineered a Python transformation pipeline to clean text-based currency strings (`£`, `$`, `¥`) and dynamically harmonize all valuations into a single base currency (£) for cross-market comparison.
2. **Predictive Pricing Models:** Trained isolated Random Forest regressors in R for the London and Tokyo markets to identify key pricing drivers and calculate Mean Absolute Error (MAE) for market predictability.
3. **Statistical Testing:** Executed Welch's t-tests and calculated Cohen's d effect sizes to mathematically prove the impact of Room Type and Superhost status on pricing and guest satisfaction.
4. **AI Sentiment Analysis (Micro-Batching):** Engineered a custom NLP pipeline to read and score the emotional sentiment of >2.1 million written guest reviews. 

## Infrastructure & Execution Strategy
**Containerization vs. Bare-Metal Execution:** A `Dockerfile` is provided for containerized execution of the baseline ELT pipeline (`clean_listings.py`). However, due to the massive scale of the NLP text processing (2.1M+ records) and the risk of CPU thermal throttling or WHEA hardware interrupts on standard local machines, the primary AI pipeline (`src/analytics/sentiment.py`) was engineered to run natively. It utilizes a custom micro-batching architecture with enforced hardware-cooling pauses, ensuring 100% data processing success without system degradation.

## Repository Structure
* `data/raw/` - Compressed, original source files from Inside Airbnb.
* `data/processed/` - The compiled DuckDB data warehouse and finalized Parquet files.
* `src/transformation/` - Python ELT scripts for cleaning and currency conversion.
* `src/analytics/` - Python scripts for NLP sentiment scoring.
* `src/analysis/` - R scripts for Random Forest modeling and statistical hypothesis testing.