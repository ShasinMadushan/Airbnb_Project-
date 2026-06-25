import pandas as pd
import duckdb
import os

def clean_price(price_str):
    """Removes $ and commas, converts to float."""
    if pd.isna(price_str):
        return None
    return float(str(price_str).replace('$', '').replace(',', ''))

def clean_listings():
    print("Loading raw listings...")
    raw_path = "data/raw/london_listings.csv.gz"
    
    # Load data
    df = pd.read_csv(raw_path, compression='gzip', low_memory=False)
    
    print("Cleaning data...")
    # 1. Standardize Price
    df['price'] = df['price'].apply(clean_price)
    df = df.dropna(subset=['price'])
    
    # 2. Parse Dates (converting to standard datetime)
    df['host_since'] = pd.to_datetime(df['host_since'], errors='coerce')
    df['last_scraped'] = pd.to_datetime(df['last_scraped'], errors='coerce')
    
    # 3. Handle a few basic missing values for cleaner analytics later
    df['name'] = df['name'].fillna("Unknown")
    df['host_name'] = df['host_name'].fillna("Unknown")
    
    # Select only the columns we actually need for analysis (keeps DB small and fast)
    cols_to_keep = [
        'id', 'name', 'host_id', 'host_name', 'host_since', 'host_is_superhost',
        'neighbourhood_cleansed', 'latitude', 'longitude', 'property_type',
        'room_type', 'accommodates', 'bedrooms', 'beds', 'price', 
        'number_of_reviews', 'review_scores_rating'
    ]
    
    df_clean = df[cols_to_keep]
    
    print("Saving to DuckDB...")
    os.makedirs("data/processed", exist_ok=True)
    db_path = "data/processed/airbnb.duckdb"
    
    # Connect to DuckDB and save the dataframe as a table
    with duckdb.connect(db_path) as con:
        # Create or replace the table
        con.execute("CREATE OR REPLACE TABLE listings AS SELECT * FROM df_clean")
        
        # Verify it worked
        count = con.execute("SELECT count(*) FROM listings").fetchone()[0]
        print(f"Successfully loaded {count} clean records into DuckDB.")

if __name__ == "__main__":
    clean_listings()